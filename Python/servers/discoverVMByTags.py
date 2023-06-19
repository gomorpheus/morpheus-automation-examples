import requests, urllib3, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# define vars for API
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}
searchTag="CreatedBy"

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
    else:
        print(f"VM: {name} deleted successfully")

def removeServer(id,name):
    url=f"https://{host}/api/servers/{id}?removeResources=off"
    r = requests.delete(url, headers=headers, verify=False)
    data = r.json()
    time.sleep(30)
    result = verify(id,name) if data['success'] else f"Remove Server func: {data}"
    print(result)
    
        

# Get all discovered VM
def getalldiscoveredvms():
    print("Get a list of discovered VM's\n")
    url=f"https://{host}/api/servers?managed=false&max=1" 
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    l = len(data['servers'])
    if l is None:
        print("No discovered servers found")
    else:
        print("Total number of discovered servers "+ str(l) + ".\n")
        for i in range(0, l):
            totalTags = len(data['servers'][i]['tags'])
            tags = data['servers'][i]['tags']
            print(f"Total Tags found on VM {data['servers'][i]['name']}: {totalTags}")
            found = False
            if totalTags is not None:
                for tag in tags:
                    if tag.get("name") == searchTag:
                        found = True
                        break
                
                if found:
                    print(f"Converting server {data['servers'][i]['name']} to managed")
                else:
                    print(f"Removing vm: {data['servers'][i]['name']}: {totalTags} from morpheus management.")
                    removeServer(data['servers'][i]['id'],data['servers'][i]['name'] )
            else:
                print(f"No Tags found on the server: {data['servers'][i]['name']}. Removing server from morpheus management")
                removeServer(data['servers'][i]['id'],data['servers'][i]['name'] )
## Main
getalldiscoveredvms()