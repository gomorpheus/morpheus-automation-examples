#!/bin/bash

echo "installing jq"
yum install epel-release -y
yum update -y
yum install jq -y

echo "Updating firewall to allow connectivity over selected port"
port="<%=customOptions.mcPort%>"
# firewall-cmd --zone=public --permanent --add-port=$port/tcp
# firewall-cmd --reload

echo "Creating minecraft user"
useradd -r -s /bin/false minecraft
chown -R minecraft:minecraft /opt/minecraft

cd /opt/minecraft
echo "Installing Java 11"
yum install -y java-11-openjdk screen
url=$(curl "<%=customOptions.mcVersion%>" |  jq -r '.downloads.server.url')
echo "Downloading Minecraft"
wget $url
echo "Making Minecraft jar executable."
chmod +x server.jar

echo "Attempting to start Minecraft Server"
systemctl enable minecraft
systemctl start minecraft
