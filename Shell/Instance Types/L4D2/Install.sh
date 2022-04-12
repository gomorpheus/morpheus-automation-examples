####################################
# Install L4D2

adduser l4d2
echo "<%=cypher.read('secret/L4D2')%>" | passwd --stdin l4d2

yum install screen glibc.i686 libstdc++.i686 -y

mkdir /L4D2 2>/dev/null
mkdir /L4D2/Morpheus 2>/dev/null
cd /L4D2/

####################################
# Install L4D2
wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
tar xf steamcmd_linux.tar.gz
rm -f steamcmd_linux.tar.gz

./steamcmd.sh +login anonymous +force_install_dir '/L4D2/Server' +app_update 222860 -validate +quit

####################################
# Install Metamod

cd /L4D2/Server/left4dead2/
wget https://mms.alliedmods.net/mmsdrop/1.10/mmsource-1.10.7-git971-linux.tar.gz
tar xf mmsource-1.10.7-git971-linux.tar.gz
rm -f mmsource-1.10.7-git971-linux.tar.gz

####################################
# Install Sourcemod

cd /L4D2/Server/left4dead2/
wget https://sm.alliedmods.net/smdrop/1.10/sourcemod-1.10.0-git6497-linux.tar.gz
tar xf sourcemod-1.10.0-git6497-linux.tar.gz
rm -f sourcemod-1.10.0-git6497-linux.tar.gz

####################################
# Create Symlinks

ln -sf /L4D2/Morpheus/server.cfg /L4D2/Server/left4dead2/cfg/server.cfg
ln -sf /L4D2/Morpheus/banned_user.cfg /L4D2/Server/left4dead2/cfg/banned_user.cfg
ln -sf /L4D2/Morpheus/banned_ip.cfg /L4D2/Server/left4dead2/cfg/banned_ip.cfg
ln -sf /L4D2/Morpheus/motd.txt /L4D2/Server/left4dead2/motd.txt
ln -sf /L4D2/Morpheus/metamod.vdf /L4D2/Server/left4dead2/addons/metamod.vdf
ln -sf /L4D2/Morpheus/host.txt /L4D2/Server/left4dead2/host.txt
ln -sf /L4D2/Morpheus/admins_simple.ini /L4D2/Server/left4dead2/addons/sourcemod/configs/admins_simple.ini

####################################
# Fix Ownership

sudo chown -R l4d2 /L4D2/

####################################
# Start Server

#su l4d2

#/L4D2/Server/srcds_run -game left4dead2 +exec server.cfg +port "<%=customOptions.steamPort%>" +maxplayers 8 -tickrate 100 -pingboost 2 +map c1m1_hotel > /dev/null 2>&1 &