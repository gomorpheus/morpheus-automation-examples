#!/bin/bash -x

select_os(){

# OSX
  if [ -f "/usr/bin/sw_vers" ]; then
   OS_RELEASE="osx"
   OS_VERSION=$(sw_vers | awk '/^ProductVersion:/ { print $2 }' | cut -d. -f1,2)

# Ubuntu, Redhat & Amazon version 7
  elif [ -f "/etc/os-release" ]; then
   OS_RELEASE=$(grep -e '^ID=' /etc/os-release | cut -d "=" -f 2 | tr -d '"')
   OS_VERSION=$(grep -e '^VERSION_ID=' /etc/os-release | cut -d "=" -f 2 | tr -d '"')

# Redhat, CentOS 6
  elif [ -f "/etc/redhat-release" ]; then
    if [ -f "/etc/centos-release" ]; then
      OS_RELEASE="centos"
      OS_VERSION=$(cat /etc/centos-release | cut -d ' ' -f 3)
    else
      OS_RELEASE="rhel"
      OS_VERSION=$(cat /etc/redhat-release | cut -d ' ' -f 7)
    fi

# Debian
  elif [ -f "/etc/debian_version" ]; then
   OS_RELEASE="debian"
   OS_VERSION=`cat /etc/debian_version`
  
  else
   OS_RELEASE=""
   echo "Unable to determine OS flavor of this machine, this OS is not supported by Morpheus."
   echo "OS hint: $OSTYPE"
   echo "Please report this error to https://support.morpheusdata.com to determine supportability of this OS."
   exit 1

  fi
}

select_os
