import requests
from morpheuscypher import Cypher
c = Cypher(morpheus=morpheus)

cyuser=str(c.get("secret/nowuser"))
cypass=str(c.get("secret/nowpass"))
task=morpheus['customOptions']['incident']
state=morpheus['customOptions']['state']
assgroup=morpheus['customOptions']['incidentgroup']
shortdescription=morpheus['customOptions']['shortdescription']
comments=morpheus['customOptions']['comments']

url = 'https://dev113361.service-now.com/api/now/table/incident_task/%s' % (task)

user = cyuser
pwd = cypass

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

jbody={"state":task,"assignment_group":assgroup,"short_description":shortdescription,"comments":comments}
body=json.dumps(jbody)
response = requests.patch(url, auth=(user, pwd), headers=headers ,data=body)

# Decode the JSON response into a dictionary and use the data
data = response.json()
print("Task " + task + "updated.")