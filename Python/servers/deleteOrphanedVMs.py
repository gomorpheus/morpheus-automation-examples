#The script will find all discovered vm's which are in the power state off
# It would then delete the vm from morpheus but not from hypervisor. It is just deleting the vm record from morpheus 
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

def getListofDiscoveredVM():
    url = ("https://%s/api/servers?serverType=vmware&powerState=off&max=1&offset=0") % (host)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    serverName = data['servers'][0]['name']
    serverId = data['servers'][0]['id']
    status = data['servers'][0]['status']
    powerState = data['servers'][0]['status']

    print("VM : %s with server id %s is in the state %s and the power status is %s") % (serverName,serverId,status,powerState)

#Main
getListofDiscoveredVM()