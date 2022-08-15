import requests
import json
#py2
from urllib import urlencode
#py3
#from urllib.parse import urlencode
tenant=morpheus['customOptions']['tenant']
group=morpheus['customOptions']['groupName']
coreCompany=morpheus['customOptions']['coreCompany']
sottosistema=morpheus['customOptions']['sottosistema']

bearerToken=morpheus['morpheus']['apiAccessToken']
host=morpheus['morpheus']['applianceHost']
morphheaders = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + (bearerToken)} 

from morpheuscypher import Cypher
c = Cypher(morpheus=morpheus,ssl_verify=False)

cypass=str(c.get("secret/dxcsnowpass"))
serviceNowInstanceName="regionetoscanatest.service-now.com"

user = 'morpheus'
pwd = cypass
headers = {"Content-Type":"application/json","Accept":"application/json"}
#Get list of cloud access
clouds=[]

def createTenant():
    url="https://%s/api/accounts" % (host)
    b={"account": {"name": tenant,"description": "Created via API","role": {"id": 2},"currency": "EUR"}}
    body=json.dumps(b)
    response = requests.post(url, headers=morphheaders, data=body, verify=False)
    data = response.json()
    tenantID=data['account']['id']
    return tenantID

def createSubtenantAdminUser(tenantID):
    print("Creating subtenant user")
    url="https://%s/api/accounts/%s/users" % (host, tenantID)
    print("Url : "+ url)
    b={"user":{"username": "testuser","email": "testuser@morpheusdata.com","firstName": "Test","lastName": "User","password": "aStr0ngp@ssword","roles": [{"id": 74}]}}
    body=json.dumps(b)
    response = requests.post(url, headers=morphheaders, data=body, verify=False)
    data = response.json()
    
# generate password
# get access token of the st user
def getAccessToken(tenantID):
    header={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
    url="https://%s/oauth/token?grant_type=password&scope=write&client_id=morph-api" % (host)
    user=str(str(tenantID) + "\\testuser")
    b = {'username': user, 'password': 'aStr0ngp@ssword'}
    body=urlencode(b)
    response = requests.post(url, headers=header, data=body, verify=False)
    data = response.json()
    access_token = data['access_token']
    return access_token

# Create a default group with the same name as tenant name
def getGroupName(access_token):
    url="https://%s/api/groups" % (host)
    headers={"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + (access_token)} 
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    print(data['groups'])

    for i in data['groups']:
        for k,v in i.items():
            if k == 'id':
                value = json.loads(str(v))
                #remove existing groups which are added by default
                url="https://%s/api/groups/%s" % (host,value)
                headers={"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + (access_token)} 
                response = requests.delete(url, headers=headers, verify=False)
    
def createGroup(access_token):
    url="https://%s/api/groups" % (host)
    headers={"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + (access_token)} 
    b = {"group": {"name": group,"code": None,"location": None}}
    body = json.dumps(b)
    response = requests.post(url, headers=headers, data=body, verify=False)
    data = response.json()


# Create tenant record in ServiceNow
def createTenantCI():
    jbody={"name":tenant,"company":coreCompany,"u_sottosistema_cctt":sottosistema}
    body=json.dumps(jbody)
    print(body)
    url='https://%s/api/now/table/u_cmdb_ci_tenant' % (serviceNowInstanceName)
    r = requests.post(url, auth=(user, pwd), headers=headers ,data=body)
    data = r.json()
    print(data)
    tsys_id = data['result']['sys_id']
    return tsys_id

# Create group record in ServiceNow
def createCMPGroup(tsys_id):
    jbody={"name":group,"u_tenant":tsys_id}
    body=json.dumps(jbody)
    print(body)
    url='https://%s/api/now/table/u_cmdb_ci_cmpresourcegroup' % (serviceNowInstanceName)
    r = requests.post(url, auth=(user, pwd), headers=headers ,data=body)
    data = r.json()
    print(data)
    cmgroupid = data['result']['sys_id']
    return cmgroupid

def createCypher(access_token):
    jbody={"value": access_token}
    body=json.dumps(jbody)
    url="https://%s/api/cypher/v1/secret/paas?type=string&ttl=0" % (host)
    headers={"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + (access_token)} 
    response = requests.put(url, headers=headers, verify=False)
    data = response.json()

def main():
    tenantID=createTenant()
    createSubtenantAdminUser(tenantID)
    access_token=getAccessToken(tenantID)
    getGroupName(access_token)
    createGroup(access_token)
    tsys_id=createTenantCI()
    createCMPGroup(tsys_id)
    #createCypher(access_token)


if __name__ == "__main__":
    main() 