import requests

# Input from the user form in service catalog.
location=morpheus['customOptions']['location']
public=morpheus['customOptions']['public']
servertype=morpheus['customOptions']['servertype']
env=str(morpheus['customOptions']['environment'])
plan=str(morpheus['customOptions']['plan'])
instanceTypeId=morpheus['customOptions']['instanceTypeId']
layoutId=morpheus['customOptions']['layoutId']

# Concatenating vars to get the group name. The group name will be used to do an API call to search for the group and get the id
group=str(location+"-"+public+"-"+servertype+"-"+env+"-"+plan)

# define vars for API
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}
apiUrl = 'https://%s/api/sites?phrase=%s' % (host, group)
url=str(apiUrl)

# Write a function to get the groupId
# Write a function to get the cloudId
# Write a function to get the networkId
# Write a fuction to get the storageId
# Write a function to get the resourcePool / cluster ID

# # Write a function to provision the instance and call the function from the below conditions.

print(location)
print(group )
if location == "csc" and public == "lan":
    print("CSC - LAN")
    if servertype == "app" and env == "4":
        print("CSC - LAN - App - Prod")
    elif servertype == "app" and env == "5":
        print("CSC - LAN - App - Non-Prod")
    elif servertype == "web" and env == "4":
        print("CSC - LAN - Web - Prod")
    elif servertype == "web" and env == "5":
        print("CSC - LAN - Web - Non-Prod")
    elif servertype == "db" and env == "4":
        print("CSC - LAN - DB - Prod")
    elif servertype == "db" and env == "5":
        print("CSC - LAN - DB - Non-Prod")
    elif servertype == "infra" and env == "4":
        print("CSC - LAN - Infra - Prod")
    elif servertype == "infra" and env == "5":
        print("CSC - LAN - Infra - Non-Prod")
elif location == "csc" and public == "dmz" and servertype == "app":
    print("CSC - DMZ - Prod - App and the network is CSC-DMZ-C-App")
elif location == "csc" and public == "dmz" and servertype == "web":
    print("CSC - DMZ - Prod - Web and the network is CSC-DMZ-C-Web")
elif location == "csc" and public == "dmz" and servertype == "db":
    print("CSC - DMZ - Prod - DB and the network is CSC-DMZ-C-DB")   