import requests
from morpheuscypher import Cypher
c = Cypher(morpheus=morpheus)

cyuser=str(c.get("secret/nowuser"))
cypass=str(c.get("secret/nowpass"))

url = 'https://dev113361.service-now.com/api/now/table/incident_task'

user = cyuser
pwd = cypass

headers = {"Content-Type":"application/json","Accept":"application/json"}
jbody={"short_description":"test","state":"2"}"
body=json.dumps(jbody)
response = requests.post(url, auth=(user, pwd), headers=headers ,data=body)

# Check for HTTP codes other than 200
if response.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
print(data)