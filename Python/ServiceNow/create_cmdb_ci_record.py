import requests
import json
from morpheuscypher import Cypher
#c = Cypher(morpheus=morpheus,ssl_verify=False)
cypass=morpheus['results']['svccypher']
cypass=cypass.replace('\r', '').replace('\n', '')
#Check if CI exist or not
 
serviceNowInstanceName="regionetoscanatest.service-now.com"
layoutCode=morpheus['instance']['provisionType']
# Set the request parameters
if "vmware" in layoutCode:
    ciclass="cmdb_ci_vmware_instance"
else:
    ciclass="cmdb_ci_kvm_vm_instance"
 
url = 'https://%s/api/now/table/%s' % (serviceNowInstanceName,ciclass)
 
# Eg. User name="admin", Password="admin" for this code sample.
user = 'morpheus'
#cypass=str(c.get("secret/dxcsnowpass"))
iname=morpheus['instance']['name']
hostname=morpheus['instance']['hostname']
ip=morpheus['instance']['containers'][0]['internalIp']
fqdn=morpheus['instance']['containers'][0]['server']['fqdn']
cpu=morpheus['instance']['cores']
strmemory=morpheus['instance']['memory']
memory=str(strmemory / 1024 / 1024 )
kbdiskszie=morpheus['instance']['storage']
disksize=str(kbdiskszie / 1024 / 1024 / 1024)
guestos=morpheus['instance']['container']['server']['platform']
osversion=morpheus['instance']['container']['server']['platformVersion']
#print("Environment for app is " + morpheus['apps'][0]['appContext'])
if "ambiente" in morpheus['customOptions']:
    ambiente=morpheus['customOptions']['ambiente']
else:
    ambiente=morpheus['apps'][0]['appContext']

if "serverRole" in morpheus['customOptions']:
    serverole=morpheus['customOptions']['serverRole']
else:
    serverole=next(iter(morpheus['instance']['apps'][0]['templateConfig']['tiers']))

u_status=morpheus['instance']['status']
instanceId=morpheus['instance']['id']
 
#Disk count
#l = len(data['instances'])
 
if "running" in u_status:
    status="on"
else:
    status="error"
 
def getDiskCount():
    bearerToken=morpheus['morpheus']['apiAccessToken']
    host = morpheus['morpheus']['applianceHost']
    headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + (bearerToken)}
    url="https://%s/api/instances/%s" % (host,instanceId)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    dcount = str(len(data['instance']['volumes']))
    return dcount
 
def createCI(diskcount):
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    body={"name": iname, "host_name": hostname, "fqdn": fqdn, "ip_address": ip, "cpus": cpu, "memory": memory, "state": status, "disks_size": disksize, "guest_os_fullname": guestos, "u_guest_os_version": osversion, "u_ambiente": ambiente, "u_server_role": serverole, "u_morpheus_instance_id": instanceId, "disks": diskcount}
    b=json.dumps(body)
 
    # Do the HTTP request
    response = requests.post(url, auth=(user, cypass), headers=headers ,data=b)
 
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
 
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)
 
def main():
    diskcount=getDiskCount()
    createCI(diskcount)
 
if __name__ == "__main__":
    main()