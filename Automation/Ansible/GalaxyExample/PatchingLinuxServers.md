# Patching Linux servers using Anisble with Morpheus to report on the Patching data.

### Use Case:

### Overview:

### Pre-reqs:
Morpheus version 5.3.2 +

**[Video](https://www.youtube.com/watch?v=iLDZZVEkkos)**

## Install Ansible on Morpheus App server(s)

## Install galaxy collection 
Install [mysql](https://docs.ansible.com/ansible/latest/collections/community/mysql/mysql_query_module.html) collection

Install [patching](https://galaxy.ansible.com/ataha/linux_patching) collection

## Add Ansible Integration in morpheus

## Add git integration 

## Add a task of type Ansible and refer the playbook

## Add a task of type python and refer to the updateJob.py script from git source. 

## Add the python task to a provisioning workflow.

## Add a custome instance type of Centos and attach the workflow to the layout

## Create a execution schedule in Morpheus to run on the 29th of every month at 23:45hrs

## Create a Job in Morpheus with associated python Task to updateJob

## Add a cypher in morpheus of mount secret to store the DB password

## Create patching table in morpheus DB

## Upload the patching report plugin in Morpheus

## Provision an instance 

## Execute the Ansible task to patch the Centos instance deployed

## Run the ansible task on the instance

## Generate Report