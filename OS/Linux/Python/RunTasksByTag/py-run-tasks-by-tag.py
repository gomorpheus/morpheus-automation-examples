import json
import requests
import sys

task_id = sys.argv[1]
tag_search_name = sys.argv[2]
option_field_name = sys.argv[3]
sslverify = True

morpheus_url = morpheus['morpheus']['applianceUrl']
token = morpheus['morpheus']['apiAccessToken']
morpheus_api = morpheus_url + "api"
instances_api = morpheus_api + "/instances"
tasks_api = morpheus_api + "/tasks/" + task_id + "/execute"

def get_by_api(api, token, sslverify):
    method = 'get'
    headers = {'Authorization': "BEARER %s" % token, "Content-Type": "application/json"}
    r = getattr(requests, method)(
        api,
        headers=headers,
        verify=sslverify
        )
    return json.loads(r.text)

def post_by_api(api, token, sslverify, payload):
    method = 'post'
    headers = {'Authorization': "BEARER %s" % token, "Content-Type": "application/json"}
    r = getattr(requests, method)(
        api,
        headers=headers,
        verify=sslverify,
        data=payload
        )
    return json.loads(r.text)

instance_response = get_by_api(instances_api, token, sslverify)

task_payload_base = { 'job': { 'targetType': 'instance' }}

for instance in instance_response['instances']:
    for tag in instance['tags']:
        if tag['name'] == tag_search_name:
            if tag['value'] == morpheus['customOptions'][option_field_name]:
                task_payload = task_payload_base
                task_payload['job']['instances'] = [instance['id']]
                jsonpayload = json.dumps(task_payload)
                post_by_api(tasks_api, token, sslverify, jsonpayload)
