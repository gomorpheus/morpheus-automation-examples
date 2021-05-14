import requests
import json

location=morpheus['customOptions']['location']
servertype=morpheus['customOptions']['servertype']

host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

def getInstanceName():
    searchName = str(location+"-"+servertype+"-"+"0")
    apiUrl = 'https://%s/api/instances?phrase=%s' % (host, searchName)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    l = len(data['instances'])
    print("Lenth of the array is "+ str(l))
    if l is None:
        print("Next availale server name is "+ searchName+"1")
        availableName = searchName+"1"
    else:
        l=l+1
        availableName=searchName+str(l)
        print("Next availale server name is " + availableName)
        return availableName

instanceName=getInstanceName()
print("Instance name is "+instanceName)              