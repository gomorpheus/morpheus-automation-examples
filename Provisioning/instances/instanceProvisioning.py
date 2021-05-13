import requests
import json

# Input from the user form in service catalog.
location=morpheus['customOptions']['location']
public=morpheus['customOptions']['public']
servertype=morpheus['customOptions']['servertype']
env=str(morpheus['customOptions']['environment'])
plan=str(morpheus['customOptions']['plan'])
layoutId=morpheus['customOptions']['layoutId']


# Concatenating vars to get the group name. The group name will be used to do an API call to search for the group and get the id
group=str(location+"-"+public+"-"+servertype+"-"+env)
print(group)

# define vars for API
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

# Write a function to get the groupId
def getGroupId():
    apiUrl = 'https://%s/api/groups?phrase=%s' % (host, group)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    groupId=data['groups'][0]['id']
    return groupId


# Write a function to get the cloudId
def getCloudId(gid):
    apiUrl = 'https://%s/api/zones?groupId=%s' % (host, gid)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    cloudId = data['zones'][0]['id']
    return cloudId


# Write a function to get the networkId
def getNetworkId(nid,zid):
    apiUrl = 'https://%s/api/networks?phrase=%s&zoneId=%s' % (host, nid, zid)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    networkid = data['networks'][0]['id']
    return networkid

# Write a fuction to get the storageId. Not required for now as all the VM's are supposed to go to a specific Datastore


# Write a function to get the resourcePool / cluster ID. This would be based on the naming logic
def getResourcePoolId(clustername,cloudId):
    apiUrl = 'https://%s/api/zones/%s/resource-pools?phrase=%s' % (host, cloudId, clustername)
    url=str(apiUrl)
    print(url)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    print(data)
    rpid = data['resourcePools'][0]['id']
    return rpid


# # Write a function to provision the instance and call the function from the below conditions.
def provision(zid,siteid,netid,clusterId):
    #JSON body of the post for instance
    jbody={"zoneId":zid,"instance":{"name":"test01","site":{"id":siteid},"type":"pbsServer","instanceContext":env,"layout":{"id":layoutId},"plan":{"id":plan},"networkDomain":{"id":null}},"config":{"resourcePoolId":clusterId,"noAgent":null,"smbiosAssetTag":null,"nestedVirtualization":"off","hostId":null,"vmwareFolderId":null,"createUser":true},"volumes":[{"id":-1,"rootVolume":true,"name":"root","size":80,"sizeId":null,"storageType":2,"datastoreId":1387}],"networkInterfaces":[{"network":{"id":netid}}]}
    #jbody={"zoneId":zid,"instance":{"name":"test02","site":{"id":siteid},"type":"centos","instanceContext":"dev","layout":{"id":402},"plan":{"id":plan},"networkDomain":{"id":None}},"config":{"resourcePoolId":clusterId,"noAgent":None,"smbiosAssetTag":None,"nestedVirtualization":"off","hostId":"","vmwareFolderId":"group-v3557","createUser":True},"volumes":[{"id":-1,"rootVolume":True,"name":"root","size":10,"sizeId":None,"storageType":1,"datastoreId":"auto"}],"networkInterfaces":[{"network":{"id":netid}}]}
    body=json.dumps(jbody)
    print(body)
    apiUrl = 'https://%s/api/instances' % (host)
    url=str(apiUrl)
    r = requests.post(url, headers=headers, data=body, verify=False)

if location == "csc" and public == "lan":
    print("CSC-LAN")
    if servertype == "app" and env == "production":
        print("CSC-LAN-App-Prod")
        networkname="TDI-DC-C-App"
        clusterName="Test, Development & Infrastructure Lab"
        #clusterName="Demo-vSAN"
        gid=getGroupId()
        print(gid)
        cid=getCloudId(gid)
        print(cid)
        nid=getNetworkId(networkname,cid)
        print(nid)
        clid=getResourcePoolId(clusterName,cid)
        print(clid)
        provision(cid,gid,nid,clid)
        #Provisioning works
        #Get the additional disks and build that up in the provision function
        #Try with different layout of different instance type. Since the function is also requested then ask for the function type selection
    elif servertype == "app" and env == "non-production":
        print("CSC - LAN - App - Non-Prod")
    elif servertype == "web" and env == "production":
        print("CSC - LAN - Web - Prod")
    elif servertype == "web" and env == "non-production":
        print("CSC - LAN - Web - Non-Prod")
    elif servertype == "db" and env == "production":
        print("CSC - LAN - DB - Prod")
    elif servertype == "db" and env == "non-production":
        print("CSC - LAN - DB - Non-Prod")
    elif servertype == "infra" and env == "production":
        print("CSC - LAN - Infra - Prod")
    elif servertype == "infra" and env == "non-production":
        print("CSC - LAN - Infra - Non-Prod")
elif location == "csc" and public == "dmz" and servertype == "app":
    print("CSC - DMZ - Prod - App and the network is CSC-DMZ-C-App")
elif location == "csc" and public == "dmz" and servertype == "web":
    print("CSC - DMZ - Prod - Web and the network is CSC-DMZ-C-Web")
elif location == "csc" and public == "dmz" and servertype == "db":
    print("CSC - DMZ - Prod - DB and the network is CSC-DMZ-C-DB")   