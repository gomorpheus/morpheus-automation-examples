#This script is to get a list of discovered type VM's, check if the plan id auto assigned by morpheus is still an existing plan, 
# if not then remove the discovered VM without removing infrastructure. 
# and let the cloud discovery get the VM again with an existing plan.

import requests

# define vars for API
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

# Get all discovered VM
def getalldiscoveredvms():
    print("Get a list of discovered VM's ")
    url="%sapi/servers?managed=false" %(host)
    r = requests.get(url, headers=headers, verify=False)
    l = len(data['servers'])
    data = r.json()
    if l is None:
        print("No discovered servers found")
    else:
        print(data)

def main():
    getalldiscoveredvms()

if __name__ == "__main__":
    main() 
