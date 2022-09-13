import json
# Declare the lifecycle and OU Name option list as a variable with contents
updatedLifecycle={"P":"PROD", "U":"UAT"}
updatedOU={"P":"Prod", "U":"NON-Prod"}

configspec = morpheus['spec']
env=configspec['customOptions']['Env']

# Check if the value if env is present in lifecycle and OU Name
if env in updatedLifecycle and env in updatedOU:
    # Set the value of lifecycle and ou name option type based on the value of env selected by user
    configspec['config']['customOptions']['LifecycleRole'] = updatedLifecycle[env]
    configspec['server']['config']['customOptions']['LifecycleRole'] = updatedLifecycle[env]
    configspec['customOptions']['customOptions']['LifecycleRole'] = updatedLifecycle[env]
    configspec['config']['customOptions']['LifecycleRole'] = updatedLifecycle[env]
    configspec['customOptions']['LifecycleRole'] = updatedLifecycle[env]
    configspec['config']['customOptions']['OUName'] = updatedOU[env]
    configspec['server']['config']['customOptions']['OUName'] = updatedOU[env]
    configspec['customOptions']['customOptions']['OUName'] = updatedOU[env]
    configspec['config']['customOptions']['OUName'] = updatedOU[env]
    configspec['customOptions']['OUName'] = updatedOU[env]
    newspec = {}
    newspec['spec'] = configspec
    newspec['spec'].pop('app', None)
    print(json.dumps(newspec))