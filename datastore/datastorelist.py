from asyncio.windows_events import NULL
import requests
from urllib.parse import urlparse
from morpheuscypher import Cypher
c = Cypher(morpheus=morpheus)

cyuser=str(c.get("secret/vcenter"))
print(cyuser)
# define vars for API

host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
cloudId=2

mainheaders = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

def getCloudUrl(host,cloudId):
    apiUrl = 'https://%s/api/zones/%s'%(host,cloudId)
    url=str(apiUrl)
    r = requests.get(url, headers=mainheaders, verify=False)
    data = r.json()
    #print(data['zone']['config']['apiUrl'])
    url_object= urlparse(data['zone']['config']['apiUrl'])
    vcenter_name= url_object.hostname
    #print(vcenter_name)
    return vcenter_name

def generateSession(vcentername):
    url = 'https://%s/api/session'%(vcentername)
    payload={}
    headers = {
  'Authorization': 'Basic bWNoYW5kQGFkLm1vcnBoZXVzZGF0YS5jb206U2hhdXJ5YUAyMDE2',
     }
    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    #print(response.text)
    return response.text

def deleteSession(vcentername,VmwareApiSessionId): 
    url = 'https://%s/api/session'%(vcentername)
    payload={}
    files={}
    headers = {
  'Authorization': 'Basic bWNoYW5kQGFkLm1vcnBoZXVzZGF0YS5jb206U2hhdXJ5YUAyMDE2',
  'Cookie': 'vmware-api-session-id='+ str(VmwareApiSessionId)
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)

    print(response.text)
 
def getDatastores(host,cloudId):
    apiUrl = 'https://%s/api/zones/%s/data-stores'% (host,cloudId)
    url=str(apiUrl)
    r = requests.get(url, headers=mainheaders, verify=False)
    data = r.json()
    datastoredetails=data['datastores']
    print("Datastoreid\t DatatstoreName\t Freespace")
    #for i in range(0, len(datastoredetails)):
     #   print(str(datastoredetails[i]['id']) +"\t"+ datastoredetails[i]['name'] +"\t"+ str(datastoredetails[i]['freeSpace']))
    return datastoredetails 

def listDatastores():
    vcentername= getCloudUrl(host,cloudId) #to fetch vcenter ip 
    print("vcenter host="+str(vcentername))

    VmwareApiSessionId =generateSession(vcentername) #create session for vcenter api calls
    Cloudatastores=getDatastores(host,cloudId)
    url = "https://%s/rest/vcenter/datastore"%(vcentername)
    payload={}
    headers = {
  'Cookie': 'vmware-api-session-id='+str(VmwareApiSessionId)
    }
    response = requests.request("GET", url, headers=headers, data=payload,verify=False)
    data=response.json()
    print("Vcenter data stores details")
    print("Datastoreid\t DatatstoreName\t Freespace\t Capacity")
  
    datastoredetails=data['value']  
    for j in range(0,len(Cloudatastores)):
        for i in range(0, len(datastoredetails)):
         #print(datastoredetails[i]['datastore'] +"\t"+datastoredetails[i]['name'] +"\t"+str(datastoredetails[i]['free_space'])+"\t"+str(datastoredetails[i]['capacity']))
            if (Cloudatastores[j]['name']==datastoredetails[i]['name']):
                percentage = (datastoredetails[i]['free_space']/datastoredetails[i]['capacity'])*100
                
                print(datastoredetails[i]['datastore'] +"\t"+datastoredetails[i]['name'] +"\t"+str(datastoredetails[i]['free_space'])+"\t"+str(datastoredetails[i]['capacity']) +"\t"+ str(percentage)) 
                #print("")
                if(percentage>=85) :
                 payload = {"datastore": { "active": False }}
                 datastoreId=Cloudatastores[j]['id']
                 url = 'https://%s/api/zones/%s/data-stores/%s'%(host,cloudId,datastoreId)
                 response = requests.put(url, json=payload, headers=mainheaders,verify=False)
                else:
                 if(Cloudatastores[j]['active']==False):
                    payload = {"datastore": { "active": True }}
                    #headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}
                    datastoreId=Cloudatastores[j]['id']
                    url = 'https://%s/api/zones/%s/data-stores/%s'%(host,cloudId,datastoreId)
                    response = requests.put(url, json=payload, headers=mainheaders,verify=False)
                    #print(response.text)
                break
               
     
    deleteSession(vcentername,VmwareApiSessionId)            





    

#call functions

listDatastores()
#getDatastores(2)
