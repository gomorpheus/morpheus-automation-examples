#The script will find all discovered vm's which are in the power state off
# It would then delete the vm from morpheus but not from hypervisor. It is just deleting the vm record from morpheus 
import requests
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

def deleteVMFromMorpheus(serverName,serverId,status,powerState):
    #This function will just delete the server record from morpheus and not from end cloud of type vmware
    url = ("https://%s/api/servers/%s?removeResources=off&preserveVolumes=off") % (host,serverId)
    r = requests.delete(url, headers=headers, verify=False)
    data = r.json()
    deleteStatus = data['success']
    print("Delete status of VM %s: %s\n\n") % (serverName,deleteStatus)

def getListofDiscoveredVM():
    url = ("https://%s/api/servers?serverType=VMware+VM&powerState=off&managed=false&max=2") % (host)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    l = len(data['servers'])
    print("Number of servers returned: %s\n") % (l)
    if l is None:
        print("No discovered vmware v's found in the powered off state. \n")
    else:
        for i in range(0, l):
            serverName = data['servers'][i]['name']
            serverId = data['servers'][i]['id']
            status = data['servers'][i]['status']
            powerState = data['servers'][i]['status']
            # Print the serverr info
            print("VM : %s with server id %s is in the state %s and the power status is %s\n") % (serverName,serverId,status,powerState)
            deleteVMFromMorpheus(serverName,serverId,status,powerState)
            



#Main
getListofDiscoveredVM()
