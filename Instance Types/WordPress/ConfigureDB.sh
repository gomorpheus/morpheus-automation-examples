RPass="<%=cypher.read('secret/mysql')%>"
WPDB="<%=customOptions.databaseName%>"
WPUser="<%=customOptions.databaseUser%>"
WPPass="<%=customOptions.databasePassword%>"

sudo mysql -u root -p$RPass -e "CREATE DATABASE $WPDB;"
sudo mysql -u root -p$RPass -e "GRANT ALL ON $WPDB.* TO $WPUser@localhost IDENTIFIED BY '$WPPass';"
sudo mysql -u root -p$RPass -e "FLUSH PRIVILEGES;"