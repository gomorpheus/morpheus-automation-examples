import requests
import sys
import json

#Variables
#bearerToken = sys.argv[1]
bearerToken=morpheus['morpheus']['apiAccessToken']
osType = morpheus['server']['osType']
platformType = morpheus['server']['platformVersion']
#windowsVersion = morpheus['results']['windowsos']
windowsVersion="2016"
morphurl = morpheus['morpheus']['applianceUrl']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + (bearerToken)} 
    
#Evaluate the OS type and version and get the job name
def getJobId():
    if osType == 'windows':
        if "2012" in windowsVersion:
            url = "%s/api/jobs?phrase=2012" % (morphurl)
            response = requests.get(url, headers=headers, verify=False)
            data = response.json()
            jobId = data['jobs'][0]['id']
            return jobId
            
        if "2016" in windowsVersion:
            url = "%s/api/jobs?phrase=2016" % (morphurl)
            response = requests.get(url, headers=headers, verify=False)
            data = response.json()
            jobId = data['jobs'][0]['id']
            return jobId
            
        if "2019" in windowsVersion:    
            url = "%s/api/jobs?phrase=2019" % (morphurl)
            response = requests.get(url, headers=headers, verify=False)
            data = response.json()
            jobId = data['jobs'][0]['id']
            return jobId
            
# Run workflow id specified in the command arguments if the osType is linux
    elif osType == 'linux':
        if "el7" in platformType:
            url = "%s/api/jobs?phrase=rhel7" % (morphurl)
            response = requests.get(url, headers=headers, verify=False)
            data = response.json()
            jobId = data['jobs'][0]['id']
            return jobId
            
        if "el8" in platformType:
            url = "%s/api/jobs?phrase=rhel8" % (morphurl)
            response = requests.get(url, headers=headers, verify=False)
            data = response.json()
            jobId = data['jobs'][0]['id']
            return jobId
            
        if "amzn2" in platformType:
            url = "%s/api/jobs?phrase=rhel7" % (morphurl)
            response = requests.get(url, headers=headers, verify=False)
            data = response.json()
            jobId = data['jobs'][0]['id']
            return jobId
        
    else:
        print('Unable to connect to API endpoint')
    
#Get the existing instances/server from the job
def getJobTargets(jobnumber):
    url = "%s/api/jobs/%s" % (morphurl, jobnumber)
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    t = data['job']['targets']
    new = "{\"refId\":"+ str(morpheus['instance']['id'])+ "}"
    t.append(json.loads(new))
    targets=json.dumps(t)
    return targets

#Update the job with the updated target list from getJobTargets()

def updateJob(jobnumber,targets):
    url="%sapi/jobs/%s" % (morphurl, jobnumber)
    body={"job": {"targetType": "instance", "targets": json.loads(targets)}}
    b = json.dumps(body)
    response = requests.put(url, headers=headers, data=b, verify=False)
    data = response.json()
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    else:
        print("Job updated successfully")
    return data
        
def main():
    jobnumber=getJobId()
    targets=getJobTargets(jobnumber)
    jobstatus=updateJob(jobnumber,targets)
    print(jobstatus)


if __name__ == "__main__":
    main() 