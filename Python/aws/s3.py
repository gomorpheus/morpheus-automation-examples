import boto3
import time
import datetime

#Setting user inputs as global vars
mbname=morpheus['customOptions']['fbname'] # user input set as bucket name
s3region=morpheus['customOptions']['fregion'] # user input set as region for bucket
musername=morpheus['username'] # user provisioning the bucket will get access to the bucket
mbservice=morpheus['customOptions']['fbunit'] # user input set as tag for the bucket
mapplication=morpheus['customOptions']['fapplication'] # user input set as tag for the bucket
flogvalue=morpheus['customOptions']['flogvalue']
user1=morpheus['customOptions']['fnoofusers']

#Get created date
today_date = datetime.date.today()
new_today_date = str(today_date.strftime("%d-%m-%Y"))

# function to create bucket
def create_bucket(bucket_name,bucket_region):
    s3_client = boto3.client('s3')
    if bucket_region == 'eu-west-1':
        s3_client = boto3.client('s3')
        s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': bucket_region
        }
    )
    else:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=bucket_name)

#Update tags to the bucket created
def set_bucket_tags(bucket,username,createdon,businessservice,application):
   s3 = boto3.resource('s3')
   bucket_tagging = s3.BucketTagging(bucket)
   response = bucket_tagging.put(
        Tagging = {
            'TagSet': [
                {
                    'Key': 'BusinessUnit', 
                    'Value': businessservice
                },
                {
                    'Key': 'Application',
                    'Value': application
                },
                {
                    'Key': 'RequestedBy',
                    'Value': username
                },
                {
                    'Key': 'CreatedOn',
                    'Value': createdon
                },
                {
                    'Key': 'CostCentre',
                    'Value': '667076'
                }
            ]    
        }
    )

#Enable versioning
def bucket_versioning(bucket_name):
    s3 = boto3.resource('s3')
    bucket_versioning = s3.BucketVersioning(bucket_name)
    response = bucket_versioning.enable()

#Setup Logging
def blogging(logboolean):
    if logboolean == 'yes':
        s3 = boto3.client('s3')
        #bucket_logging = s3.BucketLogging(mbname)
        response = s3.put_bucket_logging(
            Bucket=mbname,
            BucketLoggingStatus={
                'LoggingEnabled': {
                    'TargetBucket': mbname,
                    'TargetGrants': [
                        {
                            'Grantee': {
                                'DisplayName': 'cuxtud',
                                'EmailAddress': 'vjanish1984@gmail.com',
                                'ID': '23',
                                'Type': 'AmazonCustomerByEmail',
                                'URI': 'string'
                            },
                            'Permission': 'FULL_CONTROL'
                        },
                    ],
                    'TargetPrefix': mbname
                }
            }
        )
    else:
        print('Logging not requested')

# set encryption
def default_encryption(bucketname):
    encrypt = boto3.client('s3')
    response = encrypt.put_bucket_encryption(
        Bucket=bucketname,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                },
            ]
        },
    )


# Main
#create bucket with the name provided when Operational workflow is executed
create_bucket(mbname,s3region)
#Sleep for 10secs for the bucket to be created
time.sleep(10)
# set tags for the bukcket
set_bucket_tags(mbname,musername,new_today_date,mbservice,mapplication)
#Check if versioning is required
fbversion=morpheus['customOptions']['fbversion'] 
if fbversion == 'yes':
    bucket_versioning(mbname)
else:
    print('Versioning is not enabled')
# enable logging if reuired
blogging(flogvalue)
# enable encryption
default_encryption(mbname)