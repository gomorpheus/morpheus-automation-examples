# Activate - Deactivate datastore based on free space %

** Pre-reqs **
1. Update the cloudID in line 113
2. Update basic auth token for vcenter creds in line 32

This script will get all datastores of the cloud. It will get the vcenter url of the cloud integration and then using the vcenter session token it will fetch the total and free space of each datastore and based on the math it would activate/deactiavte the datstore for use in morpheus.

