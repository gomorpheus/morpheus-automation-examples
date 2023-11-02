#!/bin/python3
import requests
import json
import getpass
import pprint
from typing import NamedTuple
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class VirtualMachine(NamedTuple):
    uuid: str
    tag: str
    name: str
    vctrurl: str

def getVMInfo(sess, url, user,pwd):
   sessResp = sess.post(url+'/rest/com/vmware/cis/session',auth=(user,pwd))
   # The newer API after vCenter 7 Update 2 uses this format
   # sess.post(url+'/api/session',auth=(username,password))

   if sessResp.ok:
      sessionId = sessResp.json()['value']
   else:
      raise ValueError("Unable to retrieve a session ID.")    

   vmcall = sess.get(url+"/rest/vcenter/vm", headers={"vmware-api-session-id": sessionId})
   # The newer API after vCenter 7 Update 2 uses this format
   # vms=sess.get(url+'/api/vcenter/vm')
   if vmcall.ok:
      vmdump = json.loads(vmcall.text) 
      # Below is a List that we can consult
      vmLabels = vmdump["value"] 
      #print(vmLabels)
      vmTupleLst = []
      for data in vmLabels:
         vmname = data.get("name")
         vmtag = data.get("vm")
         vmidentity = sess.get(url+"/rest/vcenter/vm/"+vmtag, headers={"vmware-api-session-id": sessionId})
         if vmidentity.ok:
            vmidflds = json.loads(vmidentity.text)
            vmidtag=vmidflds["value"]["identity"]["name"]
            vmuuid=vmidflds["value"]["identity"]["instance_uuid"]
            vmTupleLst.append(VirtualMachine(vmuuid,vmtag,vmname,url))
      return vmTupleLst
   else:
      raise ValueError("Unable to retrieve VMs.")

def main():
   sess=requests.Session()
   sess.verify=False
   vsphereurl = input("vCenter URL: ")
   user = input("vCenter API Username: ")
   pwd = getpass.getpass("Password: ")
   vmDmp = getVMInfo(sess, vsphereurl,user,pwd)
   pprint.pprint(vmDmp)
   print("---")

if __name__ == "__main__":
    main()
