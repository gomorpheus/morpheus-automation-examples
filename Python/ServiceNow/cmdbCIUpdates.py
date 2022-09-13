import sys, json, requests, time
from urllib.parse import urlparse
from morpheuscypher import Cypher


# NB:
# This script takes 2 arguments 
# <%= cypher.read('secret/dxcsnowpass',true)%>
#     AND 
# <%= cypher.read('secret/cloudconfiglookuptoken',true)%>



###########
# Globals #
###########

VERBOSE = False

# Morpheus Globals
MORPHEUS_VERIFY_SSL_CERT = False
MORPHEUS_HOST = morpheus['morpheus']['applianceHost']
MORPHEUS_TENANT_TOKEN = morpheus['morpheus']['apiAccessToken']
MORPHEUS_HEADERS = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + MORPHEUS_TENANT_TOKEN} 
# MORPHEUS_IDM_NAME = "IDM"
# MORPHEUS_VCENTER_FQDN_MAP = {
#     "VMWare RTPC": "mgmtvcsa120.infra.sct.toscana.it",
#     "VMWare CCTT": "mgmtvcsa120.infra.sct.toscana.it",
#     "VMWare MGMT": "mgmtvcsa120.infra.sct.toscana.it",
#     "Default": "unknown"
# }
# MORPHEUS_VCENTER_API_VER_MAP = {
#     "VMWare RTPC": "7.0",
#     "VMWare CCTT": "7.0",
#     "VMWare MGMT": "7.0",
#     "Default": "7.0"
# }


# SNow Globals
SNOW_HEADERS = { "Content-Type": "application/json", "Accept": "application/json" }
SNOW_HOSTNAME = "regionetoscanatest.service-now.com"
SNOW_USER = 'morpheus'
# SNow password is either the 1st commandline arg like <%= cypher.read('secret/dxcsnowpass')%>
# OR Cypher secret/dxcsnowpass
if len(sys.argv) > 1:
    SNOW_PWD = sys.argv[1]
else:
    try:
        SNOW_PWD = str(Cypher(morpheus=morpheus, ssl_verify=False).get("secret/dxcsnowpass"))
    except:
        raise Exception("No SNOW password found as commandline arg or Cypher secret/dxcsnowpass..")

# Instance Globals
INSTANCE_ID = morpheus['instance']['id']
VM_NAME = morpheus['server']['name']

if "vmware" in morpheus['instance']['provisionType']:
    INSTANCE_CI_CLASS = "cmdb_ci_vmware_instance"
else:
    INSTANCE_CI_CLASS = "cmdb_ci_kvm_vm_instance"


#############
# Functions #
#############

def get_morheus_instance_detail():
    print("Fetch instance details from Morpheus...")
    url = 'https://%s/api/instances/%s' % (MORPHEUS_HOST, INSTANCE_ID)
    response = requests.get(url, headers=MORPHEUS_HEADERS, verify=MORPHEUS_VERIFY_SSL_CERT)
    if not response.ok:
        print("Error fetching instance details for ID '%s': Response code %s: %s" % (INSTANCE_ID, response.status_code, response.text))
        raise Exception("Error fetching instance details for ID '%s': Response code %s: %s" % (INSTANCE_ID, response.status_code, response.text))
 
    return response.json()    


def get_morpheus_cloud_detail(cloud_id, cloud_name):
    # Token with permissions to access cloud config info should be in master tenant at <%= cypher.read('secret/cloudconfiglookuptoken',true)%>
    # This token should be provided as the 2nd script argument
    if len(sys.argv) > 2:
        print("A second script input argument exists, using it as API bearer key...")
        morpheus_headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + sys.argv[2]}
    else:
        print("A second script input argument doesn't exist, using local API bearer key...")
        morpheus_headers = MORPHEUS_HEADERS


    print("Fetch cloud details from Morpheus...")
    url = 'https://%s/api/zones/%s' % (MORPHEUS_HOST, cloud_id)
    response = requests.get(url, headers=morpheus_headers, verify=MORPHEUS_VERIFY_SSL_CERT)
    if not response.ok:
        print("Error fetching cloud details for ID '%s': Response code %s: %s" % (cloud_id, response.status_code, response.text))
        raise Exception("Error fetching cloud details for ID '%s': Response code %s: %s" % (cloud_id, response.status_code, response.text))


    morpheus_cloud_data = response.json()
    # if the config section is missing, probably due to insufficient permissions,
    # we will attempt to get the vcenter Version and FQDN from the mapping vars at the top of the script
    if 'config' not in morpheus_cloud_data['zone']:
        print("It looks like the API key doesn't have access to get cloud config. Looking up using map vars instead...")
        cloud_name = morpheus_cloud_data['zone']['name']
        # if cloud_name in MORPHEUS_VCENTER_FQDN_MAP:
        #     vcenter_name = MORPHEUS_VCENTER_FQDN_MAP[cloud_name]
        # else:
        #     vcenter_name = MORPHEUS_VCENTER_FQDN_MAP['Default']
        #     print("Cloud '%s' not found in FQDN Map, using default '%s'." % (cloud_name, vcenter_name))

        # if cloud_name in MORPHEUS_VCENTER_API_VER_MAP:
        #     api_ver = MORPHEUS_VCENTER_API_VER_MAP[cloud_name]
        # else:
        #     api_ver = MORPHEUS_VCENTER_API_VER_MAP['Default']
        #     print("Cloud '%s' not found in API Version Map, using default '%s'." % (cloud_name, api_ver))

        # # Update config section from lookup
        # morpheus_cloud_data['zone']['config'] = {}
        # morpheus_cloud_data['zone']['config']['apiUrl'] = 'https://%s/sdk' % (vcenter_name)
        # morpheus_cloud_data['zone']['config']['apiVersion'] = api_ver
        
    return cloud_name


def get_snow_vm_sys_id():
    print("Lookup existing VM '%s' sys_id in ServiceNow..." % (VM_NAME))
    url = 'https://%s/api/now/cmdb/instance/%s' % (SNOW_HOSTNAME, INSTANCE_CI_CLASS)
    query_params = { "sysparm_query": "name=" + VM_NAME, "sysparm_limit": "1" }
    response = requests.get(url, auth=(SNOW_USER, SNOW_PWD), headers=SNOW_HEADERS, params=query_params)
    if not response.ok:
        print("Error getting instance id from ServiceNow for instance '%s': Response code %s: %s" % (VM_NAME, response.status_code, response.text))
        raise Exception("Error getting instance id from ServiceNow for instance '%s': Response code %s: %s" % (VM_NAME, response.status_code, response.text))

    data = response.json()
    result = data['result']
    if not result:
        print("Instance with name '%s' not found in ServiceNow." % (VM_NAME))
        #raise Exception("Instance with name '%s' not found in ServiceNow." % (VM_NAME))
        vm_sys_id=None
        return

    vm_sys_id = data['result'][0]['sys_id']
    print("ServiceNow Sys id for %s is %s..." % (VM_NAME, vm_sys_id))
    return vm_sys_id


def get_snow_esxi_host_sys_id(instance_data):
    print("Lookup ServiceNow sys_id for ESXi host...")
    # Get first VM details from Morpheus
    vm_id = instance_data['instance']['servers'][0]
    url = 'https://%s/api/servers/%s' %(MORPHEUS_HOST, vm_id)
    response = requests.get(url, headers=MORPHEUS_HEADERS, verify=MORPHEUS_VERIFY_SSL_CERT)
    if not response.ok:
        print("Error fetching VM details for ID %s under instance ID %s: Response code %s: %s" % (vm_id, INSTANCE_ID, response.status_code, response.text))
        raise Exception("Error fetching VM details for ID %s under instance ID %s: Response code %s: %s" % (vm_id, INSTANCE_ID, response.status_code, response.text))

    data = response.json()
    esxi_host = data['server']['parentServer']['name']
    print("...Lookup ServiceNow sys_id for ESXi host '%s'..." % (esxi_host))

    # Get SNow details for ESXI host
    url = 'https://%s/api/now/cmdb/instance/cmdb_ci_esx_server' % (SNOW_HOSTNAME)
    query_params = { "sysparm_query": "name=" + esxi_host, "sysparm_limit": "1" }
    response = requests.get(url, auth=(SNOW_USER, SNOW_PWD), headers=SNOW_HEADERS, params=query_params)
    if not response.ok:
        print("Error fetching ServiceNow ESXI Host details for '%s': Response code %s: %s" % (esxi_host, response.status_code, response.text))
        raise Exception("Error fetching ServiceNow ESXI Host details for '%s': Response code %s: %s" % (esxi_host, response.status_code, response.text))

    data = response.json()
    if not data['result']:
        print("ESXI Host '%s' not found in ServiceNow: Response code %s: %s" % (esxi_host, response.status_code, response.text))
        raise Exception("ESXI Host '%s' not found in ServiceNow: Response code %s: %s" % (esxi_host, response.status_code, response.text))

    return data['result'][0]['sys_id']


def get_snow_vcenter_sys_id(cloud_data):
    print("Lookup ServcieNow sys_id for vCenter cloud...")
    cloud_api_url = cloud_data['zone']['config']['apiUrl']
    url_object = urlparse(cloud_api_url)
    vcenter_name = url_object.hostname
    
    url = 'https://%s/api/now/cmdb/instance/cmdb_ci_vcenter' % (SNOW_HOSTNAME)
    query_params = { "sysparm_query": "name=" + vcenter_name, "sysparm_limit": "1" }
    response = requests.get(url, auth=(SNOW_USER, SNOW_PWD), headers=SNOW_HEADERS, params=query_params)
    if not response.ok:
        print("Error fetching vCenter sys_id from ServiceNow for vCenter '%s': Response code %s: %s" % (vcenter_name, response.status_code, response.text))
        raise Exception("Error fetching vCenter sys_id from ServiceNow for vCenter '%s': Response code %s: %s" % (vcenter_name, response.status_code, response.text))

    data = response.json()
    if not data['result']:
        print("vCenter '%s' not found in ServiceNow: Response code %s: %s" % (vcenter_name, response.status_code, response.text))
        raise Exception("vCenter '%s' not found in ServiceNow: Response code %s: %s" % (vcenter_name, response.status_code, response.text))

    return data['result'][0]['sys_id']   


def get_morpheus_resource_pool_name(instance_data):
    print("Lookup vCenter pool name...")

    # Token with permissions to access cloud config info should be in master tenant at <%= cypher.read('secret/cloudconfiglookuptoken',true)%>
    # This token should be provided as the 2nd script argument
    if len(sys.argv) > 2:
        print("A second script input argument exists, using it as API bearer key...")
        morpheus_headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + sys.argv[2]}
    else:
        print("A second script input argument doesn't exist, using local API bearer key...")
        morpheus_headers = MORPHEUS_HEADERS

    cloud_id = instance_data['instance']['cloud']['id']
    cloud_name = instance_data['instance']['cloud']['name']
    resource_pool_id = instance_data['instance']['containerDetails'][0]['server']['resourcePoolId']
    url = 'https://%s/api/zones/%s/resource-pools/%s' % (MORPHEUS_HOST, cloud_id, resource_pool_id)
    response = requests.get(url, headers=morpheus_headers, verify=MORPHEUS_VERIFY_SSL_CERT)
    if not response.ok:
        print("Error fetching resource pool '%s' for vCenter '%s': Response code %s: %s" % (resource_pool_id, cloud_name, response.status_code, response.text))
        raise Exception("Error fetching resource pool '%s' for vCenter '%s': Response code %s: %s" % (resource_pool_id, cloud_name, response.status_code, response.text))

    data = response.json()
    return data['resourcePool']['name']


def get_morpheus_vm_image_path(instance_data):
    print("Calculate image path...")

    # Token with permissions to access cloud config info should be in master tenant at <%= cypher.read('secret/cloudconfiglookuptoken',true)%>
    # This token should be provided as the 2nd script argument
    if len(sys.argv) > 2:
        print("A second script input argument exists, using it as API bearer key...")
        morpheus_headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + sys.argv[2]}
    else:
        print("A second script input argument doesn't exist, using local API bearer key...")
        morpheus_headers = MORPHEUS_HEADERS

    cloud_id = instance_data['instance']['cloud']['id']
    datastore_id = instance_data['instance']['containerDetails'][0]['server']['volumes'][0]['datastoreId']
    
    url = 'https://%s/api/zones/%s/data-stores/%s' % (MORPHEUS_HOST, cloud_id, datastore_id)
    response = requests.get(url, headers=morpheus_headers, verify=MORPHEUS_VERIFY_SSL_CERT)
    if not response.ok:
        print("Error fetching datastore '%s' for instance '%s': Response code %s: %s" % (datastore_id, VM_NAME, response.status_code, response.text))
        raise Exception("Error fetching datastore '%s' for instance '%s': Response code %s: %s" % (datastore_id, VM_NAME, response.status_code, response.text))

    data = response.json()
    datastore_name = data['datastore']['name']
    ipath = "[%s] %s/ %s.vmx" % (datastore_name, VM_NAME, VM_NAME)
    
    return ipath


def get_morpheus_external_vm_uuid(instance_data):
    return morpheus['server']['uuid']


def get_snow_cmp_group_sys_id():
    print("Fetch resource group sys_id...")
    group_name = morpheus['group']['name']
    url = 'https://%s/api/now/cmdb/instance/u_cmdb_ci_cmpresourcegroup' % (SNOW_HOSTNAME)
    query_params = { "sysparm_query": "name=" + group_name, "sysparm_limit": "1" }
    response = requests.get(url, auth=(SNOW_USER, SNOW_PWD), headers=SNOW_HEADERS, params=query_params)
    if not response.ok:
        print("Error fetching resource group sys_id from ServiceNow for group '%s': Response code %s: %s" % (group_name, response.status_code, response.text))
        raise Exception("Error fetching resource group sys_id from ServiceNow for group '%s': Response code %s: %s" % (group_name, response.status_code, response.text))

    data = response.json()
    if not data['result']:
        print("Resource group '%s' not found in ServiceNow: Response code %s: %s" % (group_name, response.status_code, response.text))
        raise Exception("Resource group '%s' not found in ServiceNow: Response code %s: %s" % (group_name, response.status_code, response.text))

    return data['result'][0]['sys_id']   

       
def get_snow_tenant_id():
    tenant_name = morpheus['tenant']
    print("Lookup tenant '%s' sys_id from ServiceNow..." % (tenant_name))
    url = 'https://%s/api/now/cmdb/instance/u_cmdb_ci_tenant' % (SNOW_HOSTNAME)
    query_params = { "sysparm_query": "name=" + tenant_name, "sysparm_limit": "1" }
    response = requests.get(url, auth=(SNOW_USER, SNOW_PWD), headers=SNOW_HEADERS, params=query_params)
    if not response.ok:
        print("Error fetching resource group sys_id from ServiceNow for group '%s': Response code %s: %s" % (tenant_name, response.status_code, response.text))
        raise Exception("Error fetching resource group sys_id from ServiceNow for group '%s': Response code %s: %s" % (tenant_name, response.status_code, response.text))

    data = response.json()
    if not data['result']:
        print("Resource group '%s' not found in ServiceNow: Response code %s: %s" % (tenant_name, response.status_code, response.text))
        raise Exception("Resource group '%s' not found in ServiceNow: Response code %s: %s" % (tenant_name, response.status_code, response.text))

    return data['result'][0]['sys_id']


def update_snow_instance_ci(morpheus_instance_data, morpheus_cloud_data):
    
    print("Populate general cloud fields...")
    vm_sys_id = get_snow_vm_sys_id()
    body = {}
    body["nics"] = len(morpheus_instance_data['instance']['interfaces'])
    body["correlation_id"] = str(vm_sys_id)
    body["image_path"] = get_morpheus_vm_image_path(morpheus_instance_data)
    body["u_cmp_resource_group"] = get_snow_cmp_group_sys_id()
    # body["u_tenant"] = get_snow_tenant_id() 
    if "vmware" in morpheus['instance']['provisionType']:
        print("Populate VMware fields...")
        url = 'https://%s/api/now/table/cmdb_ci_vmware_instance/%s' % (SNOW_HOSTNAME, vm_sys_id)
        # body["u_resource_pool"] = get_morpheus_resource_pool_name(morpheus_instance_data)
        # body["u_api_version"] = morpheus_cloud_data['zone']['config']['apiVersion']
        # body["vm_cluster_name"] = morpheus_instance_data['instance']['cloud']['name']
        # body["u_esx_host"] = get_snow_esxi_host_sys_id(morpheus_instance_data)
        body["vm_instance_uuid"] = get_morpheus_external_vm_uuid(morpheus_instance_data)
        # body["vcenter_ref"] = get_snow_vcenter_sys_id(morpheus_cloud_data)
    else:
        print("Populate Non-VMware fields...")
        url = 'https://%s/api/now/table/cmdb_ci_kvm_vm_instance/%s' % (SNOW_HOSTNAME, vm_sys_id)
        body["vm_inst_id"] = get_morpheus_external_vm_uuid(morpheus_instance_data)

    body_text = json.dumps(body)
    print("Updating ServiceNow @ " + url)
    print("Patch method body:")
    print(json.dumps(body, indent=4))
    
    response = requests.patch(url, auth=(SNOW_USER, SNOW_PWD), headers=SNOW_HEADERS, data=body_text)
    if not response.ok:
        print("Error updating instance CI '%s': Response code %s: %s" % (vm_sys_id, response.status_code, response.text))
        print("Patch method body:")
        print(json.dumps(body, indent=4))
        raise Exception("Error updating instance CI '%s': Response code %s: %s" % (vm_sys_id, response.status_code, response.text))

    return response.json()


# Main #

morpheus_instance_data = get_morheus_instance_detail()
if morpheus_instance_data is None:
    print("done")
    exit()
else:
    cloud_id = morpheus_instance_data['instance']['cloud']['id']
    cloud_name = morpheus_instance_data['instance']['cloud']['name']
    morpheus_cloud_data = get_morpheus_cloud_detail(cloud_id, cloud_name)
    update_snow_instance_ci(morpheus_instance_data, morpheus_cloud_data)
