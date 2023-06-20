import requests, urllib3, time, json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# define vars for API
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}
searchTag="AutomatedBy"
searchTagValue="Morpheus"

def convertToManaged(id,name):
    print (f'VM Name: {name}, VM ID: {id} will be converted to managed.\n')
    url = f'https://{ host }/api/servers/{ id }/make-managed'
    jbody={"server": {"instllAgent": False}}
    body=json.dumps(jbody)
    r = requests.put(url, headers=headers, verify=False, data=body)
    data = r.json()
    if not r.ok:
        print("Error converting to managed: Response code %s: %s" % (r.status_code, r.text))
        raise Exception("Error converting to managed: Response code %s: %s" % (r.status_code, r.text))
    else:
        print(f"Convert to manage is succesful for vm { name }.\n Checking the plan assigned..")
        time.sleep(5)

def getLicenseCount():
    url=f"https://{host}/api/license"
    r=requests.get(url, headers=headers, verify=False)
    data = r.json()
    currentUsage = data['currentUsage']['workloads']
    wleLimit=data['license']['maxInstances']
    print(f"Current usage is: {currentUsage} out of {wleLimit}")

def verify(id,name):
    url=f"https://{host}/api/servers?name={name}&max=1"
    r=requests.get(url, headers=headers, verify=False)
    data = r.json()
    size = data['meta']['size']
    if size > 0:
        #Check name
        if name == data['servers'][0]['name']:
            print(f"VM: {name} not deleted from Morpheus")
        else:
            print(f"VM: {name} deleted successfully")
            convertToManaged(id,name)
    else:
        print(f"VM: {name} deleted successfully")
        convertToManaged(id,name)

def removeServer(id,name):
    url=f"https://{host}/api/servers/{id}?removeResources=off"
    r = requests.delete(url, headers=headers, verify=False)
    data = r.json()
    time.sleep(30)
    result = verify(id,name) if data['success'] else f"Remove Server func: {data}"
    print(result)
    
# Get all discovered VM
def getalldiscoveredvms():
    getLicenseCount()
    print("Get a list of discovered VM's\n")
    url=f"https://{host}/api/servers?managed=false&max=100" 
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    serverList = []
    servernames = []
    for a in data['servers']:
        osType = a['osType']
        #print(f"server {a['name']} has osType of {osType}.")
        if 'esxi' not in a['osType']:
            #print(a['name'])
            serverList.append(a)
            servernames.append(a['name'])

    print(f"Server List:")
    for s in servernames:
        print(s)
    l = len(serverList)
    if l is None:
        print("No discovered servers found")
    else:
        print("Total number of discovered servers "+ str(l) + ".\n")
        for i in range(0, l):
            totalTags = len(serverList[i]['tags'])
            tags = serverList[i]['tags']
            print(f"Total Tags found on VM {serverList[i]['name']}: {totalTags}")
            found = False
            if totalTags != 0:
                for tag in serverList[i]['tags']:
                    if tag.get("name") == searchTag and tag.get("value") == searchTagValue:
                        found = True
                        print(f"tagname:{tag.get('name')} - tagvalue:{tag.get('value')} - found:{found}")
                        break
                if found:
                    print(f"Converting server {serverList[i]['name']} to managed")
                else:
                    print(f"Removing vm: {serverList[i]['name']}: {totalTags} from morpheus management.")
                    #removeServer(serverList[i]['id'],serverList[i]['name'] )
            else:
                print(f"No Tags found on the server: {serverList[i]['name']}. Removing server from morpheus management")

## Main
getalldiscoveredvms()
getLicenseCount()