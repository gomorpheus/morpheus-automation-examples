import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# define vars for API
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}
bid = None

def removeBuckets(bid):
    url="https://%s/api/storage/buckets/%s" % (host,bid)
    r = requests.delete(url, headers=headers, verify=False)
    if r.status_code != 200:
        print('Status:', r.status_code, 'Headers:', r.headers, 'Error Response:',r.json())
        exit()

def getBuckets():
    url="https://%s/api/storage/buckets?max=200" % (host)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    l = len(data['storageBuckets'])
    if l is None:
        print("No buckets found")
    else:
        print("Total number of discovered buckets "+ str(l) + ".\n")
        for i in range(0, l):
            bucketType = data['storageBuckets'][i]['providerType']
            if bucketType == "google":
                print("Bucket " + str(data['storageBuckets'][i]['name']) + " found of type Google Cloud Storage bucket.")
                print("Removing the bucket " + (data['storageBuckets'][i]['name']))
                bid = data['storageBuckets'][i]['id']
                removeBuckets(str(bid))

# Main
getBuckets()

