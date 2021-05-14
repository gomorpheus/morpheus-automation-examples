import requests
import json

location=morpheus['customOptions']['location']
#public=morpheus['customOptions']['public']
servertype=morpheus['customOptions']['servertype']

host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

def getInstanceName():
    x=1
    generatedName = str(location+"-"+servertype+"-"+"0"+str(x))
    print(generatedName)
    apiUrl = 'https://%s/api/instances?phrase=%s' % (host, generatedName)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    print(data)
    instances = data['instances']
    print(instances)
    for i in range(len(instances)):
        print(instances[i]['name'])
        name=instances[i]['name']
        if name == generatedName:
            for y in range(1,10):
                y=y+x
                print(y)
                generatedName = str(location+"-"+servertype+"-"+"0"+str(y))
                print(name)
                print(generatedName)
                if name == generatedName:
                    print ("Server "+name+" exists..")
                    return generatedName
                    print(generatedName)
                    
                print("Exiting..")
                quit()

instanceName=getInstanceName()
print(instanceName)              