# File Template for the Minecraft Server Start Script

| Name             	| Minecraft Start Script    	|
|------------------	|---------------------------	|
| File Name        	| start_minecraft_server.sh 	|
| File Path        	| /usr/local/bin            	|
| Phase            	| Post Provision            	|
| File Owner       	| minecraft                 	|
| Setting Name     	| start_minecraft_server.sh 	|
| Setting Category 	| Service                   	|

```
#!/usr/bin/env bash

#Standard Minecraft
cd /opt/minecraft
exec java -Xmx6144M -Xms6144M -jar server.jar nogui
```
