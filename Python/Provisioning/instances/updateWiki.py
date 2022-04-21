####
#This script will fetch the users apiToken, appliance host and update some content on the instance wiki page
#collecting data about appliance
import requests
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
instanceid=morpheus['instance']['id']
user=morpheus['instance']['createdByUsername']
jbody={"page": {"content": "**Instance Details**\r\n\r\nProvisioned by: %s \r\nProject: someproject\r\nOwner: Jane Doe\r\n\r\n**Support hours**\r\n8am to 8pm GMT\r\n\r\n**Support days**\r\nMonday to Sunday" % user} } 
body=json.dumps(jbody)
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}
apiUrl = 'https://%s/api/instances/%d/wiki' % (host, instanceid)
url=str(apiUrl)

#API request to update the Wiki page
r = requests.put(url, headers=headers, data=body, verify=False)