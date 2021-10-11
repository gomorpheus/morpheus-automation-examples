# minecraft-morpheus-deploy

This project details how to deploy a minecraft server from Morpheus utilizing the Morpheus default CentOS 7 image deployed to a vCenter. This can be done via Azure or AWS as well, buit this buildout will be done in a home lab.

If you want to get to the creation more quickly, you can use the attached Postman collection to generate all of the file templates, instance type, tasks etc...

In order to use the collection you will need to configure the following variables at the root of the collection:
-   morph_api: This is the base URL of your Morpheus appliance (Example: morpheus.domain.com)
-   morph_bearer: The API bearer token for an Administrative Morpheus user
-   git_integration_id: The ID of the git integration that is tied to this repository in Morpheus
-   op_user_name: This is you minecraft username. Used to Op your account on the Minecraft Server
-   op_user_uuid: This is the UUID of your Minecraft account. This is required for Opping your account in the ops.json file

If you want, the postman collection can create a group and attach a vCenter cloud as well with variables sepcific to the vCenter
## Requirements

-   A Morpheus server version 5.2.x or higher
-   A vCenter server connected as a cloud in Morpheus
-   This repository added a git integration in Morpheus
-   Network connectivity from Morpheus to the internet to be able to pull the Morpheus image from an S3 bucket
-   User local linux  account configured with password for system access after deployment

### Setup

This setup is assuming all requirements are already met so will not go over adding the vCenter cloud or the git integration.


#### Automation

##### Tasks
-   From the Provisioning -> Automation -> Tasks tab, you need to create 1 task. Find the configuration for this under the automation directory
    -   Install Minecraft Server

##### Workflows
-   From the Provisioning -> Automation -> Workflows tab, you need to create 1 Privisioning Workflow. The the configuration for this under the automation directory
    - Install Minecraft Server
#### Library

##### File Templates

-   From the Provisioning -> Library -> File Template tab, you need to create 5 file templates. Find the configurations for these under the file templates directory
    -   Minecraft EULA
    -   Minecraft Service
    -   Minecraft Opped Users
    -   Minecraft Server Properties
    -   Minecraft Scripts

##### Option Lists
-   From the Provisioning -> Library -> Option Lists tab, you need to create 3 option lists. Find the configuration for these under the option lists directory
    -   Minecraft Game Modes
    -   Minecraft Ports
    -   Minecraft Versions

##### Option Types
-   From the Provisioning -> Library -> Option Types tab, you need to create 3 option types. Find the configuration for these under the the option types directory
    -   Minecraft Game Mode
    -   Minecraft Port
    -   Minecraft Version

##### Instance Type
-   From the Provisioning -> Library -> Instance Types tab, you need to create 1 new instance type. Find the configuration for this under the instance configuration directory
    -   Minecraft Server

##### Instance Layout
-   Within the new instance type you need to configure a layout. Find the configuration for this under the instance configuration directory
    -   Single

##### Node Type
-   Within the new layout, you need to create a node type. Find the configuration for this under the instance configuration directory
    -   MC on CentOS7
