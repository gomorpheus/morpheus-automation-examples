URL="<%=customOptions.websiteUrl%>"
ShortURL="${URL#www.}"

cp /etc/httpd/conf.d/ssl.conf /etc/httpd/conf.d/ssl.conf.old

yum -y install python-certbot-apache

certbot certonly --webroot -w /var/www/html/ --renew-by-default --email BungeBash@gmail.com --text --agree-tos -d $URL -d $ShortURL

sudo crontab -e
0 0 * * 0 /usr/bin/certbot renew >> /var/log/certbot-renew.log