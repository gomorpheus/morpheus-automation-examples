#Updates hostname based on the instance name. 
# Strips out the first 4 characters from the instance name and use that as hostname. 
# It also gets the memory size selected by user during provisining, calculates the second disk size to be used as paging disk based on memory
# Calculatin : 1.5 X memory + 1GB

import json, requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
configspec = morpheus['spec']
 
osname = configspec['hostName']
newname = osname[4]:
configspec['hostName'] = newname
configspec['computedHostName'] = newname
configspec['instance']['hostName'] = newname
configspec['computedName'] = newname
configspec['customOptions']['hostName'] = newname
# Fetch the plan id. API call to get plan details, parse the memory and decide the value of the second disk
DISK_MEMORY_MAP = {
    "4" : "7",
    "8" : "13",
    "16" : "25",
    "32" : "49",
    "64" : "97"
}
planId = str(configspec['plan']['id'])
bearerToken=morpheus['morpheus']['apiAccessToken']
host=morpheus['morpheus']['applianceHost']
morphheaders = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + (bearerToken)} 
url="https://%s/api/service-plans/%s" % (host,planId)
response = requests.get(url, headers=morphheaders, verify=False)
data = response.json()
planMemoryKb = int(data['servicePlan']['maxMemory'])
planMemoryGB = round(planMemoryKb / 1024 /1024 / 1024) 


if str(planMemoryGB) in DISK_MEMORY_MAP:
    configspec['volumesDisplay'][1]['size'] = DISK_MEMORY_MAP[str(planMemoryGB)]
    configspec['volumes'][1]['size'] = DISK_MEMORY_MAP[str(planMemoryGB)]


newspec = {}
newspec['spec'] = configspec
print(json.dumps(newspec))