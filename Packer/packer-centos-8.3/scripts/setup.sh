#!/bin/bash -e
set -e
. /tmp/os_detect.sh

# Turn off DNS lookups for SSH
echo "UseDNS no" >> /etc/ssh/sshd_config

if [[ $OS_VERSION =~ ^6 ]]; then
	if [ -z $EPEL_DOWNLOAD_URL ]; then
		echo "No EPEL_DOWNLOAD_URL was set in environment, this should be set in Packer."
		exit 1
	fi
	rpm -i "$EPEL_DOWNLOAD_URL"
	
	yum install -y git wget curl vim cloud-init cloud-utils-growpart dracut-modules-growroot
	
	while read version; do
		version=${version#*-}
		dracut -f -H /boot/initramfs-${version}.img $version
	done < <(rpm -qa kernel)
else
	yum -y install git wget curl vim cloud-init cloud-utils-growpart

	while read version; do
		version=${version#*-}
		dracut -f -H /boot/initramfs-${version}.img $version
	done < <(rpm -qa kernel)

fi

if [[ $VAGRANT  =~ true || $VAGRANT =~ 1 || $VAGRANT =~ yes ]]; then
	mkdir -pm 700 /home/vagrant/.ssh
	wget --no-check-certificate https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub -O /home/vagrant/.ssh/authorized_keys
	chmod 0600 /home/vagrant/.ssh/authorized_keys
	chown -R vagrant:vagrant /home/vagrant/.ssh
fi

echo "uname -r: $(uname -r)"
if [[ $UPDATE  =~ true || $UPDATE =~ 1 || $UPDATE =~ yes ]]; then
		yum -y upgrade
fi

echo 'SUBSYSTEM=="net", DEVPATH=="/devices/pci0000:00/0000:00:15.0/0000:03:00.0/net/ens160", NAME="eth0"
SUBSYSTEM=="net", DEVPATH=="/devices/pci0000:00/0000:00:16.0/0000:0b:00.0/net/ens192", NAME="eth1"
SUBSYSTEM=="net", DEVPATH=="/devices/pci0000:00/0000:00:17.0/0000:13:00.0/net/ens224", NAME="eth2"
SUBSYSTEM=="net", DEVPATH=="/devices/pci0000:00/0000:00:18.0/0000:1b:00.0/net/ens256", NAME="eth3"' > /etc/udev/rules.d/10-network.rules

if [[ -f /etc/sysconfig/network-scripts/ifcfg-ens160 ]]; then
  mv /etc/sysconfig/network-scripts/ifcfg-ens160 /etc/sysconfig/network-scripts/ifcfg-eth0
fi
