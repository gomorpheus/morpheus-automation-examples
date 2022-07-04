import requests, urllib3, time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get discovered VM of a cloud of VMware VM as technology
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

def checkVMPlan(vmId):
    url = f'https://{ host }/api/servers/{ vmId }'
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    planName = data['server']['plan']['name']
    vName = data['server']['name']
    print(f"VM { vName } is assigned plan { planName }.\n")


def convertToManaged(planId,vmName,vmId, planName):
    print (f'Plan ID: {planId}, VM Name: {vmName}, VM ID: {vmId}. \n')
    url = f'https://{ host }/api/servers/{ vmId }/make-managed'
    jbody={"server": {"plan": {"id": planId}}, "instllAgent": False}
    body=json.dumps(jbody)
    r = requests.put(url, headers=headers, verify=False, data=body)
    data = r.json()
    if not r.ok:
        print("Error converting to managed: Response code %s: %s" % (response.status_code, response.text))
        raise Exception("Error converting to managed: Response code %s: %s" % (response.status_code, response.text))
    else:
        print(f"Convert to manage is succesful for vm { vmName }.\n Checking the plan assigned..")
        time.sleep(10)
        checkVMPlan(vmId)



def getServicePlan(priceSetId, vmName, zoneName, vmId):
    url = f'https://{ host }/api/service-plans?includeZones=true&provisionTypeId=6'
    r = requests.get(url, headers = headers, verify = False)
    data = r.json()
    l = len(data['servicePlans'])
    for i in range(0, l):
        p = len(data['servicePlans'][i]['priceSets'])
        for x in range(0, p):
            if priceSetId == data['servicePlans'][i]['priceSets'][x]['id']:
                print(f"Plan { data['servicePlans'][i]['name'] } should be assigned to vm { vmName } as it has a priceSet { data['servicePlans'][i]['priceSets'][x]['name'] } mapped to cloud { zoneName }.\n")
                planId = data['servicePlans'][i]['id']
                planName = data['servicePlans'][i]['name']
                convertToManaged(planId, vmName, vmId, planName)

def matchPriceSetforZoneId(zoneId, zoneName, vmName, vmId):
    url = f'https://{ host }/api/price-sets?includeZones=true&phrase=CS_vmware'
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    l = len(data['priceSets'])
    for i in range(0, l):
        if zoneId == data['priceSets'][i]['zone']['id']:
            print(f"Price set { data['priceSets'][i]['name'] } is mapped to cloud { zoneName } for vm { vmName }. Now we need to get the right plan for vm { vmName }.\n " )
            priceSetId = data['priceSets'][i]['id']
            getServicePlan(priceSetId, vmName, zoneName, vmId)

# Get discovered VM of all clouds with VMwareVM (type : vCenter) as technology
def getDiscoveredVM():    
    url = f'https://{ host }/api/servers?managed=false&serverType=Vmware+VM&max=1'
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    l = len(data['servers'])
    if l is None:
        print("No discovered servers found. \n")
    else:
        for i in range(0, l):
            vmId = data['servers'][i]['id']
            vmName = data['servers'][i]['name']
            vmZoneId = data['servers'][i]['zone']['id']
            vmZoneName = data['servers'][i]['zone']['name']
            # Search all price sets where the zoneId matches. This is to make sure that this discovered vm will be assigned a plan which is dedicated to its cloud.
            matchPriceSetforZoneId(vmZoneId, vmZoneName, vmName, vmId)

### Main
getDiscoveredVM()