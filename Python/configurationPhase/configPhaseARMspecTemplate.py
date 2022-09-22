import json, requests
#This task will be run in the config phase. I have used this for a custom instance type Azure ARM, layout windows 2016. the layout has a provisioning workflow attached with 
# this task in the configuration phase. This script will get the infrastructure group Id from the morpheus spec. Using the group id it will do an api to fetch the 
# information of the group where we parse the location from the response. The location value is then assigned to the  parameters where location is used in spec and the the 
# entire spec is printed out. 
#print(json.dumps(morpheus['spec'], indent=2))
MORPHEUS_VERIFY_SSL_CERT = False
MORPHEUS_HOST = morpheus['morpheus']['applianceHost']
MORPHEUS_TENANT_TOKEN = morpheus['morpheus']['apiAccessToken']
MORPHEUS_HEADERS = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + MORPHEUS_TENANT_TOKEN} 
GROUPID = morpheus['spec']['group']['id']

url = 'https://%s/api/groups/%s' % (MORPHEUS_HOST, GROUPID)
response = requests.get(url, headers=MORPHEUS_HEADERS, verify=MORPHEUS_VERIFY_SSL_CERT)
data = response.json()
groupLocation = data['group']['location']

configspec = morpheus['spec']
configspec['config']['templateParameter']['location'] = groupLocation
configspec['templateParameter']['location'] = groupLocation
newspec = {}
newspec['spec'] = configspec
print(json.dumps(newspec))