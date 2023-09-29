#! /usr/bin/env python3
"""
This script is thinked to run on Morpheus appliance.
It retrieves a list of instances and check if a specific
tag is present, if not then add the tag with the value 'pending'
else pass.

The script takes as 3 arguments in input:
    - ServiceNow Password <%= cypher.read('secret/dxcsnowpass',true)%>
    - Morpheus Token <%= cypher.read('secret/cloudconfiglookuptoken',true)%>
    - ServiceNow Environment can be [dev, test, prod]
"""

import sys
import json
import time
import requests
import traceback

from pprint import pprint
from urllib.parse import urlparse
from morpheuscypher import Cypher

requests.packages.urllib3.disable_warnings()

class MorpheusHandler:
    """
    Class to handle Morpheus
    """

    def __init__(self, morpheus):
        self.host  = morpheus.get('morpheus', {}).get('applianceHost')
        self.token = morpheus.get('morpheus', {}).get('apiAccessToken')
        self.headers = {
            "Content-Type"  : "application/json",
            "Accept"        : "application/json",
            "Authorization" : "Bearer " + self.token
        }
        self.idm_name = "IDM"
        self.vcenter_fqdn_map = {
            "VMWare RTPC" : "mgmtvcsa120.infra.sct.toscana.it",
            "VMWare CCTT" : "mgmtvcsa120.infra.sct.toscana.it",
            "VMWare MGMT" : "mgmtvcsa120.infra.sct.toscana.it",
            "Default"     : "unknown"     
        }

        self.vcenter_api_version = {
            "VMWare RTPC" : "7.0",
            "VMWare CCTT" : "7.0",
            "VMWare MGMT" : "7.0",
            "Default"     : "7.0" 
        }
        self.verify_ssl_cert = False
        pass

    def get_instances(self):
        """
        Retrieve the list of instances from Morpheus.
        For each instance set a tag: cmdb_update if no presente.
        """
        print("Get list of instances")
        url      = "https://%s/api/instances" % (self.host)
        response = requests.get(
            url,
            headers = self.headers,
            # params  = { "max" : 2 }, # Only for testing
            verify  = self.verify_ssl_cert
        )
        data = response.json()

        instances = []
        print(f"Number of instances found: {len(data['instances'])}")
        for instance in data.get('instances', []):
            morph_instance = MorpheusInstance(instance, morph_handler)
            morph_instance.check_tag()
            instances.append(morph_instance)

        return instances
    
    def get_cloud_detail(self, instance):
        """
        Retrieves cloud details
        """
        if len(sys.argv) > 2:
            self.headers["Authorization"] = f"Bearer {sys.argv[2]}"

        print("Fetch cloud details from Morpheus...")
        url      = 'https://%s/api/zones/%s' % (self.host, instance.cloud_id)
        response = requests.get(url, headers=self.headers, verify=self.verify_ssl_cert)
        if not response.ok:
            msg = "Error fetching cloud details for ID '%s': Response code %s: %s" % (instance.cloud_id, response.status_code, response.text)
            print(msg)
            raise Exception(msg)

        morpheus_cloud_data = response.json()

        # if the config section is missing, probably due to insufficient permissions,
        # we will attempt to get the vcenter Version and FQDN from the mapping vars at the top of the script
        if 'config' not in morpheus_cloud_data['zone']:
            print("It looks like the API key doesn't have access to get cloud config. Looking up using map vars instead...")
            cloud_name = morpheus_cloud_data['zone']['name']
            if cloud_name in self.vcenter_fqdn_map:
                vcenter_name = self.vcenter_fqdn_map[cloud_name]
            else:
                vcenter_name = self.vcenter_fqdn_map['Default']
                print("Cloud '%s' not found in FQDN Map, using default '%s'." % (cloud_name, vcenter_name))

            if cloud_name in self.vcenter_api_version:
                api_ver = self.vcenter_api_version[cloud_name]
            else:
                api_ver = self.vcenter_api_version['Default']
                print("Cloud '%s' not found in API Version Map, using default '%s'." % (cloud_name, api_ver))

            # Update config section from lookup
            morpheus_cloud_data['zone']['config'] = {}
            morpheus_cloud_data['zone']['config']['apiUrl'] = 'https://%s/sdk' % (vcenter_name)
            morpheus_cloud_data['zone']['config']['apiVersion'] = api_ver
            
        self.headers["Authorization"] = f"Bearer {self.token}"
        return morpheus_cloud_data
    
    def get_resource_pool_name(self, instance):
        """
        Retrieves ResourcePool from Morpheus
        """
        if len(sys.argv) > 2:
            self.headers["Authorization"] = f"Bearer {sys.argv[2]}"

        resource_pool_id = instance.details['instance']['containerDetails'][0]['server']['resourcePoolId']

        url = 'https://%s/api/zones/%s/resource-pools/%s' % (self.host, instance.cloud_id, resource_pool_id)
        response = requests.get(url, headers=self.headers, verify=self.verify_ssl_cert)
        if not response.ok:
            msg = "Error fetching resource pool '%s' for vCenter '%s': Response code %s: %s" % (resource_pool_id, instance.cloud_name, response.status_code, response.text)
            print(msg)
            raise Exception(msg)

        data = response.json()
        self.headers["Authorization"] = f"Bearer {self.token}"
        return data['resourcePool']['name']
    
    def get_vm_image_path(self, instance):
        """
        Retrieves image_path of an instance from Morpheus
        """
        print("Calculate image path...")
        if len(sys.argv) > 2:
            self.headers["Authorization"] = f"Bearer {sys.argv[2]}"

        cloud_id     = instance.details['instance']['cloud']['id']
        datastore_id = instance.details['instance']['containerDetails'][0]['server']['volumes'][0]['datastoreId']
        
        url = 'https://%s/api/zones/%s/data-stores/%s' % (self.host, cloud_id, datastore_id)
        response = requests.get(url, headers=self.headers, verify=self.verify_ssl_cert)
        if not response.ok:
            msg = "Error fetching datastore '%s' for instance '%s': Response code %s: %s" % (datastore_id, instance.vm_name, response.status_code, response.text)
            print(msg)
            raise Exception(msg)

        data = response.json()
        datastore_name = data['datastore']['name']
        self.headers["Authorization"] = f"Bearer {self.token}"     
        return "[%s] %s/ %s.vmx" % (datastore_name, instance.vm_name, instance.vm_name)

class MorpheusInstance:
    """
    Class that represent a morpheus instance
    """

    def __str__(self):
        return f"{vars(self)}"

    def __init__(self, instance: dict, morpheus: MorpheusHandler):
        """
        Class initializer
        """
        self.details           = instance
        self.instance_id       = instance.get('id')
        self.vm_name           = instance.get('name')
        self.group_name        = instance.get('group', {}).get('name')
        self.provision_type    = instance.get('layout', {}).get('provisionTypeCode') 
        self.instance_ci_class = self.get_ci_class()
        self.tags              = instance.get('tags', [])
        self.morpheus          = morpheus
        self.details           = self.get_instance_detail()
        self.cloud_id          = instance.get('cloud', {}).get('id')
        self.cloud_name        = instance.get('cloud', {}).get('name')
        self.nics              = instance.get('interfaces', [])
        self.sys_id            = self.get_sys_id_tag()
        self.tenant_name       = instance.get('tenant', {}).get('name')
        self.tenant_id         = instance.get('tenant', {}).get('id')
        self.datacenter        = instance.get('customOptions', {}).get('dc')
        self.external_uuid     = instance.get('containerDetails', [{}])[0].get('server', {}).get('uuid', instance.get('uuid'))
        self.disk_count        = str(len(instance.get('volumes', [])))

    def get_sys_id_tag(self):
        """
        Check if the istance has a tag called sys_id
        """
        for tag in self.tags:
            if 'sys_id' in tag.get('name', ''):
                return tag.get('value')
        return None

    def get_ci_class(self):
        """
        Return the ci class
        
        :return string
        """
        return "cmdb_ci_vmware_instance" if "vmware" in self.provision_type else "cmdb_ci_kvm_vm_instance"
    
    def check_tag(self):
        """
        Check if the instance has the proper tag
        """
        print(f"Check if the instance {self.vm_name} has the cmdb tag")

        for tag in self.tags:
            if tag['name'] == 'cmdb_update':
                print(f"cmdb update tag exist for this instance. The cmdb update is currently marked as {tag['value']}")
            else:
                print("CMDB Update tag doesn't exist on this instance. Running the cmdb update.")
                self.set_tag("pending")

        # if self.tags == []:
        #     self.set_tag("pending")

    def set_tag(self, value: str):
        """
        Set a specific tag for the Morpheus instance
        """
        print(f"Setting tag: {value}")
        url      = f"https://{self.morpheus.host}/api/instances/{self.instance_id}"
        jbody    = {"instance": {"addTags": [{"name": "cmdb_update","value": value}]}}
        body     = json.dumps(jbody)
        response = requests.put(
            url, 
            headers = self.morpheus.headers,
            data    = body,
            verify  = self.morpheus.verify_ssl_cert
        )
        return response.json()

    def get_instance_detail(self):
        """
        Retrieve instance details from Morpheus
        """
        print("Fetch instance details from Morpheus...")
        url      = f"https://{self.morpheus.host}/api/instances/{self.instance_id}"
        response = requests.get(
            url,
            headers = self.morpheus.headers,
            verify  = self.morpheus.verify_ssl_cert
        )

        if not response.ok:
            msg = "Error fetching instance details for ID '%s': Response code %s: %s" % (self.instance_id, response.status_code, response.text)
            print(msg)
            raise Exception(msg)
    
        return response.json() 

class SnowHandler:
    """
    Class to handle ServiceNow
    """

    hostnames = {
        "test"     : "regionetoscanatest.service-now.com",
        "dev"      : "regionetoscanadev.service-now.com",
        "prod"     : "regionetoscana.service-now.com"
    }

    def __init__(self, morpheus):
        """
        The init function initialize some useful vars
        for this object.
        """
        self.headers = {
            "Content-Type" : "application/json", 
            "Accept"       : "application/json"
        }
        self.user = 'morpheus'
        self.password = self.get_password()
        self.hostname = self.get_hostname()
        self.morpheus = morpheus
        pass

    def get_hostname(self):
        """
        Check if the number of arguments is correct.

        :return hostname
        """
        if len(sys.argv) < 3 or sys.argv[3] not in self.hostnames:
            raise Exception("Specificare nel task Library -> Task -> cmdb discovery -> COMMAND ARGUMENTS l'ambiente di Service Now corretto, puo' essere: test, dev, prod")

        return self.hostnames[sys.argv[3]]
    
    def get_password(self):
        """
        Check if the password is passed as argument.

        :return password
        """
        if len(sys.argv) > 1:
            password = sys.argv[1]
        else:
            try:
                password = str(Cypher(morpheus=self.morpheus, ssl_verify=False).get("secret/dxcsnowpass"))
            except:
                raise Exception("No SNOW password found as commandline arg or Cypher secret/dxcsnowpass..")
        return password
    
    def get_from_snow(self, url: str, params: dict):
        """
        General method to retrieve data from ServiceNow

        :return data
        """
        response = requests.get(
            url,
            auth    = (self.user, self.password),
            headers = self.headers,
            params  = params
        )
        if not response.ok:
            raise Exception(f"GET request failed cause: {response.text}")

        return response.json().get('result')
    
    def load_instance(self, instance, morph_handler: MorpheusHandler):
        """
        Load the data on ServiceNow
        """
        morpheus_cloud_data = morph_handler.get_cloud_detail(instance)
        time.sleep(5)

        print("Populate general cloud fields...")
        if "vmware" in instance.provision_type:
            ci = CIvmware(instance, morpheus_cloud_data, self)
        else:
            ci = CIkvm(instance, self)

        print("Updating ServiceNow @ " + ci.url)
        
        body = json.dumps(ci.to_json())
        response = requests.patch(
            ci.url, 
            auth    = (self.user, self.password),
            headers = self.headers, 
            data    = body
        )

        pprint(body)
        if response.ok:
            print(f"CI upated successfuly for instance : {instance.vm_name} Setting cmdb_update tag")
            instance.set_tag("completed")

class CI:
    """
    Represents the CI class
    """

    def __init__(self, instance, snow_handler: SnowHandler):
        """
        Initialize useful vars
        """
        if not hasattr(self, 'instance_ci_class'):
            self.instance_ci_class = "cmdb_ci_vm_instance"

        self.snow_handler   = snow_handler
        self.instance       = instance
        self.sys_id         = self.get_vm_sys_id()
        self.nics           = len(instance.nics)
        self.image_path     = self.get_image_path()
        self.u_cmp_resource_group = self.get_cmp_group_sys_id()
        self.u_tenant       = self.get_tenant_id() 
        self.u_datacenter   = self.get_datacenter_id()
        self.url            = f'https://{snow_handler.hostname}/api/now/table/{self.instance_ci_class}/{self.sys_id}'
        pass

    def get_image_path(self):
        """
        Return the image path of the instance
        """
        if self.instance.details.get('instance', {}).get('containerDetails', [{}])[0].get('server', {}).get('volumes', [{}])[0].get('datastoreId'):
            return self.instance.morpheus.get_vm_image_path(self.instance)

    def to_json(self):
        """
        Return a json based on the object
        """
        body = {
            "nics"                   : self.nics,
            "image_path"             : self.image_path,
            "u_cmp_resource_group"   : self.u_cmp_resource_group,
            "u_tenant"               : self.u_tenant,
            "u_datacenter"           : self.u_datacenter,
            "u_morpheus_instance_id" : self.instance.instance_id,
            "ip_address"             : self.instance.details['instance']['containerDetails'][0]['internalIp'],
            "fqdn"                   : self.instance.details['instance']['containerDetails'][0]['externalFqdn'],
            "cpus"                   : self.instance.details['instance']['containerDetails'][0]['server']['maxCores'],
            "memory"                 : str(self.instance.details['instance']['containerDetails'][0]['server']['maxMemory'] / 1024 / 1024 ),
            "state"                  : "error" if "failed" in self.instance.details['instance']['status'] else "on",
            "disks_size"             : str(self.instance.details['instance']['containerDetails'][0]['server']['maxStorage'] / 1024 / 1024),
            "guest_os_fullname"      : self.instance.details['instance']['containerDetails'][0]['server']['platform'],
            "u_guest_os_version"     : self.instance.details['instance']['containerDetails'][0]['server']['platformVersion'],
            "name"                   : self.instance.details['instance']['name'],
            "host_name"              : self.instance.details['instance']['containerDetails'][0]['server']['hostname'],
            "u_ambiente"             : self.instance.details['instance'].get('instanceContext',""),
            "u_server_role"          : self.instance.details['instance'].get("customOptions", {}).get("serverRole", ""),
            "u_self_managed"         : 'true' if self.instance.details['instance'].get("customOptions", {}).get("managedtype", "") == 'self-managed' else 'false',
            "u_base_plus"            : self.instance.details['instance'].get("customOptions", {}).get("supportlevel", ""),
            "u_service_offering"     : self.instance.details['instance'].get("customOptions", {}).get("computetype"),
            "short_description"      : self.instance.details['instance'].get("instance", {}).get("description", "")
        }
        if instance.disk_count:
            body.update({"disks" : self.instance.disk_count})
        return body

    def get_vm_sys_id(self):
        """
        Retrieves vm sys_id
        """
        if self.instance.sys_id:
            return self.instance.sys_id

        url   = f'https://{snow_handler.hostname}/api/now/cmdb/instance/{self.instance.instance_ci_class}'
        params = { 
            "sysparm_query" : f"install_status!=7^name={self.instance.vm_name}",
            "sysparm_limit" : "1"
        }
        result = self.snow_handler.get_from_snow(url, params)

        if not result:
            print("Instance with name '%s' not found in ServiceNow." % (self.instance.vm_name))
            raise Exception("The CMDB discovery script in the master tenant has not yet been executed on this instance server record")

        vm_sys_id = result[0]['sys_id']
        print("ServiceNow Sys id for '%s' is '%s' ..." % (self.instance.vm_name, vm_sys_id))
        return vm_sys_id
    
    def get_cmp_group_sys_id(self):
        """
        Retrieves cmp_group_sys_id from ServiceNow
        """
        url = 'https://%s/api/now/cmdb/instance/u_cmdb_ci_cmpresourcegroup' % (snow_handler.hostname)
        params = {
            "sysparm_query" : f"name={self.instance.group_name}", 
            "sysparm_limit" : "1"
        }
        result = self.snow_handler.get_from_snow(url, params)
        if not result:
            msg = "Resource group '%s' not found in ServiceNow" % (instance.group_name)
            print(msg)
            raise Exception(msg)

        return result[0]['sys_id']
    
    def get_tenant_id(self):
        """
        Retrieves Tenant ID from ServiceNow
        """

        print("Lookup tenant '%s' sys_id from ServiceNow..." % (self.instance.tenant_name))
        url = 'https://%s/api/now/cmdb/instance/u_cmdb_ci_tenant' % (self.snow_handler.hostname)
        params = {
            "sysparm_query" : f"name={self.instance.tenant_name}",
            "sysparm_limit" : "1"
        }
        result = self.snow_handler.get_from_snow(url, params)
        if not result:
            msg = "Tenant '%s' not found in ServiceNow" % (self.instance.tenant_nam)
            print(msg)
            raise Exception(msg)

        return result[0]['sys_id']
    
    def get_datacenter_id(self):
        """
        Retrieves Datacenter ID from ServiceNow
        """
        if not self.instance.datacenter:
            self.instance.datacenter = None
            raise Exception("Datacenter not specified")

        url    = 'https://%s/api/now/table/cmdb_ci_datacenter' % (self.snow_handler.hostname)
        params = {
            "sysparm_query" : f"name={self.instance.datacenter}",
            "sysparm_limit" : "1"
        }
        result = self.snow_handler.get_from_snow(url, params)
        if not result:
            msg = "Datacenter '%s' not found in ServiceNow: Response code %s: %s" % (self.instance.datacenter)
            print(msg)
            raise Exception(msg)

        return result[0]['sys_id'] 


class CIvmware(CI):
    """
    Represents the Vmware CI
    """

    def __init__(self, instance, cloud_data: dict, snow_handler: SnowHandler):
        """
        Use Superclass initializer
        """
        self.instance_ci_class = "cmdb_ci_vmware_instance"
        super().__init__(instance, snow_handler)
        self.u_resource_pool  = instance.morpheus.get_resource_pool_name(instance)
        self.u_api_version    = cloud_data['zone']['config']['apiVersion']
        self.vm_cluster_name  = instance.cloud_name
        self.u_esx_host       = self.get_esxi_host_sys_id()
        self.vm_instance_uuid = instance.external_uuid
        self.vcenter_ref      = self.get_vcenter_sys_id(cloud_data)

    def to_json(self):
        """
        Return a json based on the object
        """
        body = super().to_json()
        body.update({
            "u_resource_pool" : self.u_resource_pool,
            "u_api_version"   : self.u_api_version,
            "vm_cluster_name" : self.vm_cluster_name,
            "u_esx_host"      : self.u_esx_host,
            "vm_instance_uuid": self.vm_instance_uuid,
            "vcenter_ref"     : self.vcenter_ref
        })
        return body


    def get_esxi_host_sys_id(self):
        """
        Retrieves ESXI host sys_id from ServiceNow
        """
        print("Lookup ServiceNow sys_id for ESXi host...")

        vm_id = self.instance.details['instance']['servers'][0]
        url = 'https://%s/api/servers/%s' %(self.instance.morpheus.host, vm_id)
        response = requests.get(
            url,
            headers = self.instance.morpheus.headers,
            verify  = self.instance.morpheus.verify_ssl_cert
        )
        if not response.ok:
            msg = "Error fetching VM details for ID %s under instance ID %s: Response code %s: %s" % (vm_id, self.instance.instance_id, response.status_code, response.text)
            print(msg)
            raise Exception(msg)

        data = response.json()
        esxi_host = data['server']['parentServer']['name']

        print("...Lookup ServiceNow sys_id for ESXi host '%s'..." % (esxi_host))
        url = 'https://%s/api/now/cmdb/instance/cmdb_ci_esx_server' % (self.snow_handler.hostname)
        params = {
            "sysparm_query" : f"name={esxi_host}",
            "sysparm_limit" : "1"
        }
        result = self.snow_handler.get_from_snow(url, params)
        if not result:
            msg = "ESXI Host '%s' not found in ServiceNow: Response code %s: %s" % (esxi_host, response.status_code, response.text)
            print(msg)
            raise Exception(msg)

        return result[0]['sys_id']
    
    def get_vcenter_sys_id(self, cloud_data):
        """
        Retrieves vcenter sys_id from ServiceNow
        """
        print("Lookup ServcieNow sys_id for vCenter cloud...")
        cloud_api_url = cloud_data['zone']['config']['apiUrl']
        url_object   = urlparse(cloud_api_url)
        vcenter_name = url_object.hostname
        
        url    = 'https://%s/api/now/cmdb/instance/cmdb_ci_vcenter' % (self.snow_handler.hostname)
        params = {
            "sysparm_query" : f"name={vcenter_name}",
            "sysparm_limit" : "1"
        }
        result = self.snow_handler.get_from_snow(url, params)
        if not result:
            msg = "vCenter '%s' not found in ServiceNow" % (vcenter_name)
            print(msg)
            raise Exception(msg)

        return result[0]['sys_id'] 

class CIkvm(CI):
    """
    Represents the KVM CI
    """

    def __init__(self, instance, snow_handler: SnowHandler):
        """
        Use Superclass initializer
        """
        self.instance_ci_class = "cmdb_ci_kvm_vm_instance"
        super().__init__(instance, snow_handler)
        self.vm_inst_id  = instance.external_uuid

    def to_json(self):
        """
        Return a json based on the object
        """
        body = super().to_json()
        body.update({
            "vm_inst_id" : self.vm_inst_id
        })
        return body

VERBOSE = False

if __name__ == "__main__":    
    morph_handler = MorpheusHandler(morpheus)
    snow_handler  = SnowHandler(morpheus)

    instances = morph_handler.get_instances()

    for instance in instances:
        try:
            snow_handler.load_instance(instance, morph_handler)
        except Exception as e:
            print(f"Can't load {instance}, cause: {e}, full traceback: {traceback.format_exc()}")
    
    print("Done")