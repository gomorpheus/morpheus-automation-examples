import boto3, requests, urllib3, sys
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

role = 'OrganizationAccountAccessRole'
creds = []
morphurl = sys.argv[4]
apitoken = sys.argv[1]

#Instantiate 'organization' object
org_client = boto3.client('organizations',
	aws_access_key_id=sys.argv[2],
    aws_secret_access_key=sys.argv[3])

#instantiate 'sts' object
sts_client = boto3.client('sts',
	aws_access_key_id=sys.argv[2],
    aws_secret_access_key=sys.argv[3])

#Call list_accounts() method on organization object
org_response = org_client.list_accounts()

#Iterate through listed accounts
for i in range(0, int(len(org_response['Accounts']))):
	#Instantiate datetime account was added to org
	added = org_response['Accounts'][i]['JoinedTimestamp']
	#Instantiate account name
	name = org_response['Accounts'][i]['Name']
	
	if (added.date() - datetime.today().date()).days == -1: #If the account was added to the organization on the prior date (yesterday)
		#Instantiate the ID for the AWS account currently being iterated on
		current = org_response['Accounts'][i]['Id']
	else:
		#Skip to the next iteration if the currently considered account was not added to the organization in the last day
		continue

	#Run assume_role() method on sts object
	sts_response = sts_client.assume_role(
		RoleArn=f'arn:aws:iam::{current}:role/{role}',
		RoleSessionName='mySession')

	#Append the temporary creds/role arn as a tuple to a list called 'creds'
	creds.append((name, 
		#sts_response['Credentials']['AccessKeyId'],  
		#sts_response['Credentials']['SecretAccessKey'], 
		#sts_response['Credentials']['SessionToken'], 
		sts_response['AssumedRoleUser']['Arn']))

#Iterate through each tuple in creds
for cred in creds:
	#Attempt to integrate a new cloud with Morpheus using the temporary creds from assumerole using Morpheus API
	requestHeaders = {'Content-type': 'application/json', 
		'Authorization': f'Bearer {apitoken}'}

	requests.post(f'{morphurl}/api/zones', 
		json={
			"zone": {
				"name": cred[0], 
				"description": None, 
				"groupId": 1, 
				"zoneType": {
					"code": "amazon"
				},
				"config": {
					"certificateProvider": "internal", 
					"endpoint": "ec2.us-east-1.amazonaws.com", 
					"accessKey": sys.argv[2], 
					"secretKey": sys.argv[3],
					"stsAssumeRole": cred[1], 
					"vpc": "All", 
					"importExisting": "off"
				},
				"code": None,
				"location": None,
				"visibility": "private"
				}
			},
		headers=requestHeaders, 
		verify=False)
