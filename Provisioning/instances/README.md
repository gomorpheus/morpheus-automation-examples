## instanceProvisioning.py

This is in service catalog. Catalog Item type operational workflow.

This is smart workload placement. Based on the different values selected on the form https://d.pr/i/Te3H3D, the  functions will determine the correct Group, Cloud, Network, ResourcePool, Datastore, verify if the instance name exist in morpheus, if yes then increment the sequence and provision the instance.

Once the instance is successfully provisioned it will show up in service catalog under inventory.

On the morpheus app server run:

yum install mysql-devel gcc gcc-devel python-devel