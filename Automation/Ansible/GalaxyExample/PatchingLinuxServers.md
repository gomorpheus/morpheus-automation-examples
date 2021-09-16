# Patching Linux servers using Anisble with Morpheus to report on the Patching data.

### Use Case:
When a user deploys an instance *in this use case we are referring to Centos 7* from Morpheus, based on the Operating system and version the instance should be added to a patching job. The job is scheduled to run on the 29th of every month at 23:45hrs. The job runs an ansible playbook on all the servers attached, the play patching the OS to latest verion. The patching results (success, failed, noChanges) are then recorded in Morpheus. A custom report type (report template) is added to generate a report on the patching results.

This use case is an example of the level of customization and User friendly UI with RBAC that can be done.

![alt text](https://github.com/gomorpheus/morpheus-automation-examples/blob/main/src/common/images/Patching_new.png "Flow")

<dd>The above image shows the flow of user self service provisioning. User submits the instance provisioning of a Centos VM via Morpheus UI/API. The 
 
**[Video](https://www.youtube.com/watch?v=iLDZZVEkkos)**

## Pre-reqs:
Morpheus v5.3.2 +
[Download](https://morpheushub.com/download)

[Install Ansible](https://docs.morpheusdata.com/en/latest/integration_guides/Automation/ansible.html#id1) on Morpheus App server(s)
Ubuntu
```
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```
Centos
```
sudo yum install epel-release
sudo yum install ansible
```
Then create the working Ansible directory for Morpheus
```
sudo mkdir /opt/morpheus/.local/.ansible
sudo chown -R morpheus-app.morpheus-local /opt/morpheus/.local/.ansible
```

[Install Python on Morpheus App Server(s)](https://morpheus.lightning.force.com/lightning/r/Knowledge__kav/ka04N0000003V32QAE/view) *python tasks wont run if this pre-reqs is not completed.*

## Install galaxy collection 
Install [mysql](https://docs.ansible.com/ansible/latest/collections/community/mysql/mysql_query_module.html) collection
Install [patching](https://galaxy.ansible.com/ataha/linux_patching) collection

...Run the below commands on morpheus app server(s) as **root**:

```
yum install python3-devel mysql-devel python3-pip python3-pymysql -y
pip3 install mysqlclient
ansible-galaxy collection install ataha.linux_patching
ansible-galaxy collection install community.mysql
mv /root/.ansible/collections/ansible_collections/ataha /opt/morpheus/.local/.ansible/collections/ansible_collections/
mv /root/.ansible/collections/ansible_collections/community /opt/morpheus/.local/.ansible/collections/ansible_collections/community/
chown -R morpheus-app.morpheus-local /opt/morpheus/.local/.ansible/collections/ansible_collections/
```

## Add Ansible Integration in morpheus
[How to Doc](https://docs.morpheusdata.com/en/latest/integration_guides/Automation/ansible.html#add-ansible-integration)

<dl>
<b>Use the below values for the integration</b>
<dt>Ansible Git URL</dt> 
<dd>https://github.com/cuxtud/morpheus-ansible2.git</dd>

<dt>Default Branch</dt> 
<dd>master</dd>

<dt>Playbooks Path</dt> 
<dd>/</dd>

<dt>Roles Path</dt> 
<dd>/roles</dd>

<dt>Group Variables Path</dt> 
<dd>/group_vars</dd>

<dt>Host Variables Path</dt> 
<dd>/hosts</dd>

<dt>User MorpheusAgent Command Bus</dt> 
<dd>checked</dd>
</dl>

![alt text](https://github.com/gomorpheus/morpheus-automation-examples/blob/main/src/common/images/AddAnsibleIntegration.png "Ansible Integration")
<dl>
<dt> Save Changes </dt>
</dl>

## Add git integration 

*Add in Morpheus UI. Nagivate to Administration > Integration > Add -> Git*
<dl>
<dt> Name </dt>
<dd> Enter any name </dd>

<dt> Git Url </dt>
<dd> https://github.com/gomorpheus/morpheus-automation-examples </dd>

<dt> Default Branch </dt>
<dd> main </dd>
</dl>

![alt text](https://github.com/gomorpheus/morpheus-automation-examples/blob/main/src/common/images/gitIntegration.png "Git Integration")
<dl>
<dt> Save Changes </dt>
</dl>

## Add a task of type Ansible and refer the playbook

*In Morpheus UI, Browse to Provisioning > Automation > Tasks > Add*
<dl>
<dt> Name </dt>
<dd> <i> Enter a Name </i> </dd>

<dt> Type </dt>
<dd> Select Ansible Playbook </dd>

<dt> Ansible Repo </dt>
<dd> Select the ansible integration from the list </dd>

<dt> Playbook </dt>
<dd> patching_linux.yml </dd>

<dt> Execute Target </dt>
<dd> Resource </dd>
</dl>

![alt text](https://github.com/gomorpheus/morpheus-automation-examples/blob/main/src/common/images/AnsibleTask.png "Ansible Task")

<dl>
<dt> Save Changes </dt>
</dl>

## Add a task of type python and refer to the updateJob.py script from git source. 

<dl>
<dt> Name </dt>
<dd> <i> Enter a name </i> </dd>

<dt> Type </dt>
<dd> Select Python Script </dd>

<dt> Result Type </dt>
<dd> None </dd>

<dt> Source </dt>
<dd> Select Repository </dt>

<dt> Repository </dt>
<dd> Select the git integration </dd>

<dt> File Path </dt>
<dd> Automation/Jobs/updateJob.py </dd>

<dt> Additional Packages </dt>
<dd> requests simplejson </dd>

<dt> Execute Target </dt>
<dd> Local </dd>
</dl>

![alt text](https://github.com/gomorpheus/morpheus-automation-examples/blob/main/src/common/images/pythonTask.png "Python Task")

<dl>
<dt> Save Changes </dt>
</dl>

## Add the python task to a provisioning workflow.
In Morpheus UI, Navigate to *Provisioning > Automation > workflow > Add > Provisioing Workflow*

<dl>
<dt> Name </dt>
<dd> <i> Enter a name </i> </dd>

<dt> Provision </dt>
<dd> <i>Search for the python task and select</i></dd>
</dl>

![alt text](https://github.com/gomorpheus/morpheus-automation-examples/blob/main/src/common/images/jobUpdateWorkflow.png "Provisionin workflow")
<dl>
<dt> Save Changes </dt>
</dl>

## Add a custom instance type of Centos and attach the workflow to the layout

This [Video](https://d.pr/v/F4XWwG) demonstrates how to create:

* Instance type
* Layout
* Attach workflow to layout
* Add node type to layout

## Create an execution schedule in Morpheus 

In Morpheus UI, navigate to *Provisioning > Automation > Execute Scheduling > Add*

<dl>
<dt> Name </dt>
<dd> <i> Enter a name </i> </dd>

<dt>Time Zone</dt>
<dd><i>Select a time zone</i></dd>

<dt>Schedule</dt>
<dd>45 23 29 * *</dt>

</dl>

![alt text](https://github.com/gomorpheus/morpheus-automation-examples/blob/main/src/common/images/executionSchedule.png  "Execution Schedule")
<dl>
<dt> Save Changes </dt>
</dl>

## Create a Job in Morpheus with associated python Task to updateJob

In Morpheus UI, navigate to *Provisioning > Automation > Jobs > Add*
<dl>
<dt> Name </dt>
<dd> <i> Enter a name </i> </dd>

<dt>Job Type</dt>
<dd> Task Job</dd>

**Click Next**

<dt> Task </dt>
<dd> Select the ansible task </dd>

<dt> Schedule </dt>
<dd> Select the schedule </dd>

<dt> Context Type </dt>
<dd> Select Instance </dd>

<dt> Context Instance </dt>
<dd> Serch for an existing instance and add temporarily </dd>

**Click Next**

**Click Complete**
</dl>

## Add a cypher in morpheus of mount secret to store the DB password

*Fetch the db password for the morpheus user from the morpheus-secrets.json file in /etc/morpheus/ directory*
 In Morpheus UI, navigate to *Tools > Cypher > Add*

 <dl>
 <dt>Key</dt>
 <dd>secret/secret/dbpass<dd>

 <dt>Value</dt>
 <dd><i>Paste the password fetch from the above file</i></dd>

 <dt> Save Changes </dt>
 <dl>

## Create patching table in morpheus DB

*ssh* to Morpheus app server and run below to create table in morpheus db

```
/opt/morpheus/embedded/bin/mysql -h 127.0.0.1 -u morpheus -p
mysql> use morpheus
mysql> CREATE TABLE `patching` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `server_name` varchar(255) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `last_updated` datetime DEFAULT NULL,
  `next_run` datetime DEFAULT NULL,
  `result` varchar(255) DEFAULT NULL,
  `os` varchar(255) DEFAULT NULL,
  `env` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
```

## Upload the patching report plugin in Morpheus

[Download](https://github.com/gomorpheus/morpheus-automation-examples/blob/main/plugin/custom_report_type/build/libs/morpheus-example-reports-plugin-1.2.2.jar) the patching report plugin to your desktop

Upload in Morpheus UI, navigate to *Administration > Integrations > Plugins > Choose File > Upload*

If the upload is successful, then the screen should look like

![alt text](https://github.com/gomorpheus/morpheus-automation-examples/blob/main/src/common/images/pluginUpload.png  "Custom Report Plugin")

## Testing

**[Video](https://www.youtube.com/watch?v=iLDZZVEkkos)**