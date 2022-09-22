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
    print("Get a list of discovered VM's\n")
    url="https://%s/api/servers?managed=false&serverType=Vmware+VM&max=1" % (host)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    l = len(data['servers'])
    if l is None:
        print("No discovered servers found")
    else:
        print("Total number of discovered servers "+ str(l) + ".\n")
        for i in range(0, l):
            existingPlans=['12','13']
            if str(data['servers'][i]['plan']['id']) in existingPlans:
                print("VM " + data['servers'][i] + " is running with an existing plan.")
            else:
                print("Plan for VM "+ data['servers'][i]['name'] + " is " + str(data['servers'][i]['plan']['name']) + " and the id of the plan is " + str(data['servers'][i]['plan']['id']) + ".\nRemoving the discovered VM " + data['servers'][i]['name'] + " from morpheus without deleting the VM infrastructure. Upon Cloud sync the VM will be back in morpheus as discovered type VM." )
                url="https://%s/api/servers/%s?removeResources=off" % (host,data['servers'][i]['id'])
                r = requests.delete(url, headers=headers, verify=False)
                rdata = r.json()
                if rdata['success'] == True:
                    print("VM "+ data['servers'][i]['name'] + " successfully deleted.\n")

def main():
    getalldiscoveredvms()

if __name__ == "__main__":
    main() 
