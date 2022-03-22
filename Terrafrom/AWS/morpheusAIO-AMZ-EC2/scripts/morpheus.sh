#!/bin/bash -xe
<%=instance?.cloudConfig?.agentInstallTerraform%>
<%=cloudConfig?.finalizeServer%>
sudo wget ${download}
sudo rpm -ihv *morpheus*
sudo morpheus-ctl reconfigure