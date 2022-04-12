# File Template For the Minecraft Service

| Name             | Minecraft Service   |
|------------------|---------------------|
| File Name        | mincraft.service    |
| File Path        | /etc/systemd/system |
| Phase            | Post Provision      |
| File Owner       | minecraft           |
| Setting Name     | minecraft.service   |
| Setting Category | service             |

## Template Content
```
[Unit]
Description=Start Minecraft
After=network.target

[Service]
Type=simple
User=minecraft
ExecStart=/usr/local/bin/start_minecraft_server.sh
ExecStop=/usr/local/bin/minecraftd exit
TimeoutStartSec=30

[Install]
WantedBy=default.target
```