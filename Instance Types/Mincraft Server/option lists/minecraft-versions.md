# Configuration for the Minecraft Versions Option List

Users will select the version of minecraft they want to install on the server.

This is a rest call to the versions manifest

| Name              	| Minecraft Versions                                              	|
|-------------------	|-----------------------------------------------------------------	|
| Description       	| Rest call to display available versions of Minecraft to Install 	|
| Type              	| REST                                                            	|
| Visibility        	| Private                                                         	|
| Source URL        	| https://launchermeta.mojang.com/mc/game/version_manifest.json   	|
| Real Time         	| Yes                                                             	|
| Ignore SSL Errors 	| Yes                                                             	|
| Source Method     	| GET                                                             	|
| Headers           	| None                                                            	|

## Initial Dataset
```

```

## Translation Script
```
for(var x=0;x < data.versions.length; x++) {
  results.push({name: data.versions[x].id, value:data.versions[x].url});
}
```

## Request Script
```

```

