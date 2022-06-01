# Get all instances which have an expiry date set and send expiry notifiation remind every 22 hours. Start 72hrs from the expiry date.
import requests

# define vars for API
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

#get all instance which have an expiry date set
def getInstances():
    url="https://%s/api/instances" % (host)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    l = len(data['instances'])
    if l is None:
        print("No instances found")
    else:
        print("Total number of discovered instances "+ str(l) + ".\n")
        #for i in range(0, l):
