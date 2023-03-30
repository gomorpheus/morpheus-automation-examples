#!/bin/python3
"""
@Author: Wittling
@Date: ....
@Credit: ...
@Links: https://github.com/tryfan/pymorpheus
"""
import sys
import getpass
import requests
import pprint
import json
import argparse
import vspherevmid
from typing import NamedTuple
from urllib.parse import urlparse

# This allows us to use a specific version of the pymorpheus API
# which we have downloaded and unpacked locally.
sys.path.append( '/opt/gitbucket/nfv-morpheus-scripts/python/morpheusapi/vers015' )
#for p in sys.path:
#    print( p )
from pymorpheus import MorpheusClient

morpheusenv= [
    'dstlab', 
    'nonprod', 
    'prod'
]

class PasswordPromptAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        # If no value is given on the commandline prompt for password.
        if values:
            # Ideally a security warning could be generated here.
            setattr(args, self.dest, values)
        else:
            setattr(args, self.dest, getpass.getpass())

# Create an instance of ArgumentParser
parser = argparse.ArgumentParser(description="Morpheus vCenter Reconciliation Utility.")
parser.add_argument('--menv', nargs=1,dest='menv', required=True, choices=morpheusenv, 
                help='Morpheus Environment. (dstlab|nonprod|prod)', metavar='')
parser.add_argument('-u','--user',nargs=1,dest='user',help='Morpheus Id',required=True)      
parser.add_argument('-c', '--credential',dest='pwd',type=str, action=PasswordPromptAction, nargs='?', default='', help=argparse.SUPPRESS)
#parser.add_argument('-c','--credential',nargs=1,help='Morpheus Credential',required=True)      
parser.add_argument('--show',action='store_true',dest='show',help='print list of detected orphans',default=True)      
parser.add_argument('--remove',action='store_true',dest='remove',help='remove detected orphans from Morpheus and vCenter')      
parser.add_argument('-v', '--verbose', action='store_true',dest='verbose',default=False)  # on/off flag

args = parser.parse_args()
menv = args.menv[0]
user = args.user[0]
pwd = args.pwd
verbose = args.verbose
remove = args.remove
show = args.show

# the url in these cases is actually the LB Proxy in front of Morpheus Appliance.
# not the appliances themselves.
if menv == 'dstlab':
   morpheusUrl = 'https://something.com'
elif menv == 'nonprod':
   morpheusUrl = 'https://something.com'
elif menv == "prod":
   morpheusUrl = 'https://something.com'
else:
   morpheusUrl = 'unknown'
  
print("DBG:menv: " + menv)
print("DBG:morpheusUrl: " + morpheusUrl)
print("DBG:user: " + user)

if pwd == "":
   user_pass = {}
   complete = False
   while not complete:
      #user = input("Morpheus Username: ")
      pwd = getpass.getpass("Morpheus Password: ")

      if user in user_pass and pwd == user_pass[user]:
         print("Welcome", user)
         break
      else:
        user_pass[user]=pwd
        complete = True

morpheus = MorpheusClient(morpheusUrl, username=user, password=pwd,sslverify=False)
#morpheus = MorpheusClient(morpheusUrl, user, pwd, sslverify=False)

class MorpheusCloud(NamedTuple):
   cldid: str
   cldname: str
   cldapiurl: str
   cldapiusr: str
   cldapipwd: str

# pull the cypher data for the clouds up front. more efficient.
cyphropts = []
append = "cypher/secret/vcenters"
cyphresults = morpheus.call("get",append,options=cyphropts)
if cyphresults['success'] != True:
   raise Exception ("ERR: Cypher Call Failed")

# CLOUDS
#options = [('max','1')]
options = []
results = morpheus.call("get", "zones", options=options)

cloudTupleLst = []
for cloud in results['zones']:
    #pprint.pprint(cloud)
    cldname = cloud["name"]
    cldid = cloud["id"]
    cldcredid = cloud["credential"]["id"]
    cldapiurl = cloud["config"]["apiUrl"]
    parsed = urlparse(cldapiurl)
    baseurl = "https://" + parsed.netloc

    credopts = []
    append = "credentials" + "/" + str(cldcredid) 
    # NOTE: this call only presents a success attribute in json if the call fails.
    cldcredresults = morpheus.call("get",append,options=options)
    cldapiusr = cldcredresults["credential"]["username"]

    cldapipwd = "unknown"
    for vctr in cyphresults["data"]["vcenters"]:
       if vctr["url"] == baseurl:
          cldapipwd = vctr["cred"]
          break

    if cldapipwd == "unknown":
       raise Exception("vCenter Authentication Issue: " + cldname + ":" + baseurl)
    
    cloudTupleLst.append(MorpheusCloud(cldid,cldname,baseurl,cldapiusr,cldapipwd))

    # NOTE: refreshing the cloud is an asynchronous pub sub event. so while the 
    # call may come back success or fail, the update takes time in the background.
    refreshopts = []
    append = "zones" + "/" + str(cloud["id"]) + "/refresh"
    results = morpheus.call("post",append,options=refreshopts)
    if results['success'] != True:
       print("WARN: Cloud Refresh Failed")

# this gives us a distinct list of vCenter url endpoints so we do not repetatively vCenter VMs.
urlset = set()
sess=requests.Session()
sess.verify=False
allvctr = []
cldctr = 0
for cldinfo in cloudTupleLst:
   cldctr += 1
   if verbose == True:
      if cldctr == 1:
         print("\nMorpheus Clouds:")
      print("cloud name: %s cloud url: %s" % (cldinfo.cldname, cldinfo.cldapiurl))
   if cldinfo.cldapiurl not in urlset:
      vmDmp = vspherevmid.getVMInfo(sess,cldinfo.cldapiurl,cldinfo.cldapiusr,cldinfo.cldapipwd) 
      allvctr = allvctr + vmDmp
   urlset.add(cldinfo.cldapiurl)

# sort the list by url and print it out.
if verbose == True:
   print("\nvCenter VMs attached to Morpheus Cloud(s): ")
   pprint.pprint(sorted(allvctr, key=lambda x: (x[3], x[2]))) 
   print("")

# now sort it by uuid to expedite search
# print(sorted(allvctr, key=lambda x: x[1])) 

# INSTANCES
print("Instances: ")
#options = [('max','1')]
options = []
instcallrsp = morpheus.call("get", "instances", options=options)
#pprint.pprint(results)
instctr = 0
for instance in instcallrsp['instances']:
    instctr += 1
    pprint.pprint("--------------------------------------------------------------------------")
    print("Instance Name: %s" % instance["name"])

    # the instance only has an array of server ids. the server info itself requires an addtl API fetch 
    svrids = instance["servers"]
    
    # for each server id we shall call and get that server and we should only get one.
    for svrid in svrids:
       #print("server id: " + str(svrid))
       options = [('id', str(svrid))]
       results = morpheus.call("get", "servers", options=options)
       if results['meta']['size'] != 1:
          pprint.pprint("ERR: Server call returned unexpected number of results.")
          raise Exception("Server call returned unexpected number of results.")
       else:
          #pprint.pprint(results["servers"])
          for server in results["servers"]:
             print("Server: " + server["name"])
             idx = next((i for i, v in enumerate(allvctr) if v[0] == server["internalId"]), -1)
             orphan = False
             if idx == -1:
                orphan = True
                print("\033[32;5mORPHAN!!! UUID %s NOT Found in vCenter.\033[0m" % server["internalId"])
                if (remove == True):
                   pprint.pprint("Removing " + server["name"] + ".")
                   append = "servers" + "/" + str(server["id"]) 
                   options = [('removeResources','on'),('removeInstances','on'),('force','on')]
                   results = morpheus.call("delete", append, options=options)
                   print("DEL RESULTS")
                   pprint.pprint(results)
             else:
                print("NOT ORPHAN: UUID %s Found in vCenter." % server["internalId"])
