yum -y install sssd realmd oddjob oddjob-mkhomedir adcli samba-common samba-common-tools krb5-workstation openldap-clients policycoreutils-python

echo "<%=cypher.read('secret/domainJoinPass')%>" | realm join --user=<%=cypher.read('secret/domainJoinUser')%> "<%=container.domainName%>"

history -cw