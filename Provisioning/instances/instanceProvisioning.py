import requests
import json
import time
import sys
from urlparse import urlparse
import mysql.connector
from morpheuscypher import Cypher
from datetime import datetime
c = Cypher(morpheus=morpheus)

# Input from the user form in service catalog.
location=morpheus['customOptions']['location']
public=morpheus['customOptions']['public']
servertype=morpheus['customOptions']['servertype']
env=str(morpheus['customOptions']['environment'])
plan=str(morpheus['customOptions']['plan'])
layoutId=int(morpheus['customOptions']['layoutId'])
userInstanceName=str(morpheus['customOptions']['InstanceName'])
cypass=str(c.get("secret/dbpass"))


# Concatenating vars to get the group name. The group name will be used to do an API call to search for the group and get the id
group=str(location+"-"+public+"-"+servertype+"-"+env)
#print(group)

# define vars for API
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

def getInstanceName():
    uINameStripped = userInstanceName[0:3]
    #print(uINameStripped)
    searchName = str(location+"-"+servertype+"-"+uINameStripped+"-"+"0")
    #print(searchName)
    apiUrl = 'https://%s/api/instances?phrase=%s' % (host, searchName)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    l = len(data['instances'])
    #print("Lenth of the array is "+ str(l))
    if l is None:
        print("Next availale server name is "+ searchName+"1")
        availableName = searchName+"1"
    else:
        l=l+1
        availableName=searchName+str(l)
        print("Next availale server name is " + availableName)
        return availableName

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
    print(apiUrl)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    networkid = data['networks'][0]['id']
    return networkid

# Write a function to get the resourcePool / cluster ID. This would be based on the naming logic
def getResourcePoolId(clustername,cloudId):
    apiUrl = 'https://%s/api/zones/%s/resource-pools?phrase=%s' % (host, cloudId, clustername)
    url=str(apiUrl)
    #print(url)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    #print(data)
    rpid = data['resourcePools'][0]['id']
    return rpid

# Get DatatoreID
def getDatastoreId(cloudId,datastoreName):
    apiUrl = 'https://%s/api/zones/%s/data-stores?name=%s' % (host, cloudId, datastoreName)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    #print(data)
    dsid = data['datastores'][0]['id']
    return int(dsid)

# Get Date
def getDate():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

# Provision Instance
def provision(zid,siteid,netid,clusterId,dsId,iname):
    #JSON body of the post for instance
    ##jbody={"zoneId":zid,"instance":{"name":"test02","site":{"id":siteid},"type":"win-server","instanceContext":env,"layout":{"id":layoutId},"plan":{"id":plan},"networkDomain":{"id":None}},"config":{"resourcePoolId":clusterId,"noAgent":None,"smbiosAssetTag":None,"nestedVirtualization":"off","hostId":None,"vmwareFolderId":None,"createUser":True},"volumes":[{"id":-1,"rootVolume":True,"name":"root","size":80,"sizeId":None,"storageType":2,"datastoreId":dsId}],"networkInterfaces":[{"network":{"id":netid}}]}
    #jbody={"zoneId":zid,"instance":{"name":iname,"site":{"id":siteid},"type":"win-server","instanceContext":env,"layout":{"id":layoutId},"plan":{"id":plan},"networkDomain":{"id":None}},"config":{"resourcePoolId":clusterId,"noAgent":None,"smbiosAssetTag":None,"nestedVirtualization":"off","hostId":None,"vmwareFolderId":None,"createUser":True},"volumes":[{"id":-1,"rootVolume":True,"name":"root","size":80,"sizeId":None,"storageType":2,"datastoreId":dsId}],"networkInterfaces":[{"network":{"id":netid}}]}
    #below used by Anish in test lab
    jbody={"zoneId":zid,"instance":{"name":iname,"site":{"id":siteid},"type":"customcentos","instanceContext":"dev","layout":{"id":layoutId},"plan":{"id":plan},"networkDomain":{"id":None}},"config":{"resourcePoolId":clusterId,"noAgent":None,"smbiosAssetTag":None,"nestedVirtualization":"off","hostId":"","vmwareFolderId":None,"createUser":True},"volumes":[{"id":-1,"rootVolume":True,"name":"root","size":10,"sizeId":None,"storageType":1,"datastoreId":dsId}],"networkInterfaces":[{"network":{"id":netid}}]}
    body=json.dumps(jbody)
    #print(body)
    apiUrl = 'https://%s/api/instances' % (host)
    url=str(apiUrl)
    r = requests.post(url, headers=headers, data=body, verify=False)
    data = r.json()
    print("Response from provisioning API: ")
    print(data)
    instanceId = data['instance']['id']
    print("Instance Id: "+ str(instanceId))
    return instanceId

# Get Instance created by Id
def getCreatedById(instanceId):
    apiUrl = 'https://%s/api/instances/%s' % (host,instanceId)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    createdById = data['instance']['owner']['id']
    return createdById

#Update DB to show the instance in service catalog inventory
def updateDB(iname,getdate,instanceId,createdById):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="morpheus",password=cypass,
        database="morpheus"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO catalog_item (date_created, ref_name, last_updated, owner_id, order_date, ref_type, ref_id, quantity, type_id, created_by, status, hidden) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (getdate, iname, getdate, 1, getdate, "instance", instanceId,1, 34, createdById, "ORDERED", 0)
    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

if location == "csc" and public == "lan":
    print("CSC-LAN")
    if servertype == "app" and env == "production":
        print("CSC-LAN-App-Prod")
        networkname="vxw-dvs-555-virtualwire-109-sid-8074-CSC-DC-C-APP"
        clusterName="Business Applications"
        datastorename="FA-VVOL-BA"
        #clusterName="Demo-vSAN"
        #networkname="TDI-DC-C-App"
        #clusterName="Demo-vSAN"
        #datastorename="vsanDatastore"
        gid=getGroupId()
        #print(gid)
        cid=getCloudId(gid)
        #print(cid)
        nid=getNetworkId(networkname,cid)
        #print(nid)
        clid=getResourcePoolId(clusterName,cid)
        #print(clid)
        datastoreId=getDatastoreId(cid,datastorename)
        instanceName=str(getInstanceName())
        insId=provision(cid,gid,nid,clid,datastoreId,instanceName)
        currentDate=getDate()
        cbId=getCreatedById(insId)
        time.sleep(10)
        updateDB(instanceName,currentDate,insId,cbId)
        quit()
        #Provisioning works
        #Get the additional disks and build that up in the provision function
        #Try with different layout of different instance type. Since the function is also requested then ask for the function type selection
    elif servertype == "app" and env == "non-production":
        print("CSC - LAN - App - Non-Prod")
        networkname="vxw-dvs-8425-virtualwire-127-sid-8101-TDI-DC-C-APP"
        clusterName="Test, Development & Infrastructure Lab"
        datastorename="FA-VVOL-TDI"
        gid=getGroupId()
        cid=getCloudId(gid)
        nid=getNetworkId(networkname,cid)
        clid=getResourcePoolId(clusterName,cid)
        datastoreId=getDatastoreId(cid,datastorename)
        instanceName=str(getInstanceName())
        insId=provision(cid,gid,nid,clid,datastoreId,instanceName)
        currentDate=getDate()
        cbId=getCreatedById(insId)
        time.sleep(10)
        updateDB(instanceName,currentDate,insId,cbId)
        quit()
    elif servertype == "web" and env == "production":
        print("CSC - LAN - Web - Prod")
        networkname="vxw-dvs-555-virtualwire-108-sid-8069-CSC-DC-C-WEB"
        clusterName="Business Applications"
        datastorename="FA-VVOL-BA"
        gid=getGroupId()
        cid=getCloudId(gid)
        nid=getNetworkId(networkname,cid)
        clid=getResourcePoolId(clusterName,cid)
        datastoreId=getDatastoreId(cid,datastorename)
        instanceName=str(getInstanceName())
        insId=provision(cid,gid,nid,clid,datastoreId,instanceName)
        currentDate=getDate()
        cbId=getCreatedById(insId)
        time.sleep(10)
        updateDB(instanceName,currentDate,insId,cbId)
        quit()        
    elif servertype == "web" and env == "non-production":
        print("CSC - LAN - Web - Non-Prod")
        networkname="vxw-dvs-8425-virtualwire-124-sid-8047-TDI-DC-C-WEB"
        clusterName="Test, Development & Infrastructure Lab"
        datastorename="FA-VVOL-TDI"
        gid=getGroupId()
        cid=getCloudId(gid)
        nid=getNetworkId(networkname,cid)
        clid=getResourcePoolId(clusterName,cid)
        datastoreId=getDatastoreId(cid,datastorename)
        instanceName=str(getInstanceName())
        insId=provision(cid,gid,nid,clid,datastoreId,instanceName)
        currentDate=getDate()
        cbId=getCreatedById(insId)
        time.sleep(10)
        updateDB(instanceName,currentDate,insId,cbId)
        quit()          
    elif servertype == "db" and env == "production":
        print("CSC - LAN - DB - Prod")
        networkname="vxw-dvs-555-virtualwire-110-sid-8079-CSC-DC-C-DB"
        clusterName="Business Applications"
        datastorename="FA-VVOL-BA"
        gid=getGroupId()
        cid=getCloudId(gid)
        nid=getNetworkId(networkname,cid)
        clid=getResourcePoolId(clusterName,cid)
        datastoreId=getDatastoreId(cid,datastorename)
        instanceName=str(getInstanceName())
        insId=provision(cid,gid,nid,clid,datastoreId,instanceName)
        currentDate=getDate()
        cbId=getCreatedById(insId)
        time.sleep(10)
        updateDB(instanceName,currentDate,insId,cbId)
        quit()        
    elif servertype == "db" and env == "non-production":
        print("CSC - LAN - DB - Non-Prod")
        networkname="vxw-dvs-8425-virtualwire-128-sid-8102-TDI-DC-C-DB"
        clusterName="Test, Development & Infrastructure Lab"
        datastorename="FA-VVOL-TDI"
        gid=getGroupId()
        cid=getCloudId(gid)
        nid=getNetworkId(networkname,cid)
        clid=getResourcePoolId(clusterName,cid)
        datastoreId=getDatastoreId(cid,datastorename)
        instanceName=str(getInstanceName())
        insId=provision(cid,gid,nid,clid,datastoreId,instanceName)
        currentDate=getDate()
        cbId=getCreatedById(insId)
        time.sleep(10)
        updateDB(instanceName,currentDate,insId,cbId)
        quit()        
    elif servertype == "infra" and env == "production":
        print("CSC - LAN - Infra - Prod")
        networkname="vxw-dvs-555-virtualwire-43-sid-8037-CSC-DC-INFRASTRUCTURE"
        clusterName="Business Applications"
        datastorename="FA-VVOL-BA"
        gid=getGroupId()
        cid=getCloudId(gid)
        nid=getNetworkId(networkname,cid)
        clid=getResourcePoolId(clusterName,cid)
        datastoreId=getDatastoreId(cid,datastorename)
        instanceName=str(getInstanceName())
        insId=provision(cid,gid,nid,clid,datastoreId,instanceName)
        currentDate=getDate()
        cbId=getCreatedById(insId)
        time.sleep(10)
        updateDB(instanceName,currentDate,insId,cbId)
        quit() 
    elif servertype == "infra" and env == "non-production":
        print("CSC - LAN - Infra - Non-Prod")
        networkname="vxw-dvs-8425-virtualwire-11-sid-8010-TDI-INFRA-01"
        clusterName="Test, Development & Infrastructure Lab"
        datastorename="FA-VVOL-TDI"
        gid=getGroupId()
        cid=getCloudId(gid)
        nid=getNetworkId(networkname,cid)
        clid=getResourcePoolId(clusterName,cid)
        datastoreId=getDatastoreId(cid,datastorename)
        instanceName=str(getInstanceName())
        insId=provision(cid,gid,nid,clid,datastoreId,instanceName)
        currentDate=getDate()
        cbId=getCreatedById(insId)
        time.sleep(10)
        updateDB(instanceName,currentDate,insId,cbId)
        quit()        
        
elif location == "csc" and public == "dmz" and servertype == "app":
    print("CSC - DMZ - Prod - App and the network is CSC-DMZ-C-App")
elif location == "csc" and public == "dmz" and servertype == "web":
    print("CSC - DMZ - Prod - Web and the network is CSC-DMZ-C-Web")
elif location == "csc" and public == "dmz" and servertype == "db":
    print("CSC - DMZ - Prod - DB and the network is CSC-DMZ-C-DB") 