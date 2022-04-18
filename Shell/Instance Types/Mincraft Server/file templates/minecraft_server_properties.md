# File Template for Minecraft Server Properties

| Name             	| Minecraft Server Properties 	|
|------------------	|-----------------------------	|
| File Name        	| server.properties           	|
| File Path        	| /opt/minecraft              	|
| Phase            	| Post Provision              	|
| File Owner       	| minecraft                   	|
| Setting Name     	| server.properties           	|
| Setting Category 	| Configuration               	|

```
#Minecraft server properties
enable-rcon=true
broadcast-rcon-to-ops=true
view-distance=10
max-build-height=256
server-ip=
level-seed=
rcon.port=25575
gamemode=<%=customOptions.mcGameMode%>
server-port=<%=customOptions.mcPort%>
allow-nether=true
enable-command-block=true
enable-rcon=false
enable-query=false
op-permission-level=4
prevent-proxy-connections=false
generator-settings=
resource-pack=
level-name=world
rcon.password=<%=customOptions.mcPassword%>
player-idle-timeout=0
motd=\u00A7b\u00A7oWelcome to the World of Tomorrow!!!
query.port=25565
force-gamemode=false
hardcore=false
white-list=false
broadcast-console-to-ops=true
pvp=true
spawn-npcs=true
generate-structures=true
spawn-animals=true
snooper-enabled=true
difficulty=easy
function-permission-level=2
network-compression-threshold=256
level-type=default
spawn-monsters=true
max-tick-time=60000
enforce-whitelist=false
use-native-transport=true
max-players=20
resource-pack-sha1=
spawn-protection=0
online-mode=true
allow-flight=false
max-world-size=29999984
```