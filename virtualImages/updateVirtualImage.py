import requests
import json
import warnings
warnings.filterwarnings("ignore")

"""
This script will go through the virtual images name provided in line 11 and set the Force guest Customization check to false"
"""
bearerToken=morpheus['morpheus']['apiAccessToken']
host = morpheus['morpheus']['applianceHost']
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "Bearer " + (bearerToken)} 

updateGuestCustomization = ['DGSPPJW1001-1620993814000','DGSPPJW1001-1620993937000','DGSPPJW1001-1620995380000']

def updateVI():
    for x in updateGuestCustomization:
        url="https://%s/api/virtual-images?phrase=%s" % (host, x)
        r = requests.get(url, headers=headers, verify=False)
        data = r.json()
        vId=str(data['virtualImages'][0]['id'])
        vName=data['virtualImages'][0]['name']
        print("Updating guest customization of Virtual Image " + vName + " with associated ID: " + vId)
        updateurl="https://%s/api/virtual-images/%s" % (host, vId)
        b={"virtualImage": {"isForceCustomization": False}}
        body=json.dumps(b)
        ur = requests.put(updateurl, headers=headers, data=body, verify=False)
        udata=ur.json()
        success=udata['success']
        if success == True:
            print("Force Guest customization for virtual image " + vName + " is set to false successfully.")
        else:
            print("Force Guest customization for virtual image " + vName + " failed.")


def main():
    updateVI()


if __name__ == "__main__":
    main() 
