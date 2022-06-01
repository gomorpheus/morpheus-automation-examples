import requests

import requests

# define vars for API
host=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

def getBuckets():
    url="https://%s/api/storage/buckets" % (host)
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

def removeBuckets():
    url="https://%s/api/storage/buckets" % (host)

# Main
getBuckets()
