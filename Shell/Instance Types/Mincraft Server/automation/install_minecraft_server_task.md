# Configuration for the Install Minecraft Server Task

| Name           	| Install Minecraft Server          	|
|----------------	|-----------------------------------	|
| Code           	| installMinecraftServer            	|
| Result Type    	| None                              	|
| SUDO           	| Yes                               	|
| Source         	| Repository                        	|
| Repository     	| {{Your Integration to this Repo}} 	|
| File Path      	| automation/install_minecraft.sh   	|
| Version Ref    	| Main                              	|
| Execute Target 	| Resource                          	|

# Configuration for the Install Minecraft Server Provisioning Workflow

| Name           	| Install Minecraft Server  	|
|----------------	|---------------------------	|
| Description    	| Installs Minecraft Server 	|
| Platform       	| Linux                     	|
| Configuration  	|                           	|
| Pre Provision  	|                           	|
| Provision      	|                           	|
| Post Provision 	| Install Minecraft Server  	|
| Start Service  	|                           	|
| Stop Service   	|                           	|
| Pre Deploy     	|                           	|
| Deploy         	|                           	|
| Reconfigure    	|                           	|
| Teardown       	|                           	|
| Shutdown       	|                           	|
| Startup        	|                           	|