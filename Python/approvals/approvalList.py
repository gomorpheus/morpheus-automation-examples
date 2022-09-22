import requests, urllib3, datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Use this as an operational workflow tied to a ctalog item. An input typeof text or number requesting no of days to produce the result for. The fieldName should be noOfDays.

host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

def approvalList():
    url='https://%s/api/approvals' % (host)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    #print(data)
    ##Get the current date in format YYYY-MM-DD
    x = datetime.datetime.now()
    d = (x.strftime("%Y")+"-"+x.strftime("%m")+"-"+x.strftime("%d"))
    currentdate=str(d)
    #print("Current Date : " + currentdate)

    ##Get the start date in format YYYY-MM-DD, past 30 days
    ## The number in datetime.timedelta(30) can be set to whatever the last days report required.

    #s = datetime.datetime.now() - datetime.timedelta(30)
    s = datetime.datetime.now() - datetime.timedelta(int(morpheus['customOptions']['noOfDays']))
    sd = (s.strftime("%Y")+"-"+s.strftime("%m")+"-"+s.strftime("%d"))
    startdate=str(sd)
    #print("Start Date : " + startdate)
    approvalList = data['approvals']
    for i in data['approvals']:
        #Do an api call for each item in the approval list to get more details of the approval item. Like Approved by and the Request for values.
        #print(i)
        approvalId = str(i['id'])
        url='https://%s/api/approvals/%s' % (host,approvalId)
        r = requests.get(url, headers=headers, verify=False)
        data = r.json()
        a = data['approval']
        for k,v in a.items():
            if k == 'dateCreated':
                #print("Key is " + k)
                #print("Value is " + v)
                idate = str(v[:10])
                #print("idate is " + idate)
                if startdate <= idate <= currentdate:
                    print(a['requestType'] + " for " + a['approvalItems'][0]['reference']['name'] + " was requested by " + a['requestBy'] + " on " + a['dateCreated'] + ". Approval status is " + a['status'] + ".")
                    if a['approvalItems'][0]['approvedBy'] is None:
                        print("This was approved via ServiceNow.")
                        print("")
                    else:
                        print("The request was approved by " + a['approvalItems'][0]['approvedBy'] )
                        print("")
                    
# Main
approvalList()