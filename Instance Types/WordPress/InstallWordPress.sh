setenforce 0

yum -y install http://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum -y install epel-release yum-utils
yum-config-manager --enable remi-php73
yum -y install wget phpMyAdmin httpd mod_ssl php php-common php-mysql php-gd php-xml php-mbstring php-mcrypt

systemctl start httpd
systemctl enable httpd
firewall-cmd --add-service=http
firewall-cmd --add-service=https
firewall-cmd --runtime-to-permanent

wget http://wordpress.org/latest.tar.gz
tar xfz latest.tar.gz 
cp -rf wordpress/* /var/www/html/
rm -rf wordpress