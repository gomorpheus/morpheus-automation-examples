# Configuration for the Minecraft Server Instance Type


## Instance Type Configuration

| Name                  	| Minecraft Server                                            	|
|-----------------------	|-------------------------------------------------------------	|
| Code                  	| mcServer                                                    	|
| Description           	| Minecraft Server Instance Type                              	|
| Category              	| Apps                                                        	|
| Icon                  	|                                                             	|
| Permissions           	| Public                                                      	|
| Option Types          	| Minecraft Version List, Minecraft Game Mode, Minecraft Port 	|
| Environment Prefix    	| MC                                                          	|
| Environment Variables 	|                                                             	|
| Enable Settings       	| Yes                                                         	|
| Enable Scaling        	| No                                                          	|
| Support Deployments   	| No                                                          	|

## Layout Configuration

| Name                       	| Single                  	|
|----------------------------	|-------------------------	|
| Version                    	| 1.0                     	|
| Description                	| Minecraft Single Server 	|
| Creatable                  	| Yes                     	|
| Technology                 	| VMWare                  	|
| Minimum Memory             	| 8 GB                    	|
| Workflow                   	| Deploy Minecraft Server 	|
| Support Convert To Managed 	| No                      	|
| Enable Scaling             	| No                      	|
| Environment Variables      	|                         	|
| Option Types               	|                         	|
| Nodes                      	| MC on CentOS7           	|

## Node Configuration

| Name                 	| MC on CentOS7                                                                                                 	|
|----------------------	|---------------------------------------------------------------------------------------------------------------	|
| Short Name           	| mcOnCent7                                                                                                     	|
| Version              	| 1.0                                                                                                           	|
| Environment Variable 	|                                                                                                               	|
| VM Image             	| Morpheus CentOS 7.5 v4                                                                                        	|
| Log Folder           	|                                                                                                               	|
| Config Folder        	|                                                                                                               	|
| Deploy Folder        	|                                                                                                               	|
| Extra Options        	|                                                                                                               	|
| Service Ports        	|                                                                                                               	|
| Scripts              	|                                                                                                               	|
| File Templates       	| Minecraft Service, Minecraft Opped Users, Minecraft Server Properties, Minecraft EULA, Minecraft Start Script 	|
| Copies               	| 1                                                                                                             	|
