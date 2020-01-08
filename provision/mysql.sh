#!/usr/bin/env bash

debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
apt-get update
apt-get install -y mysql-server
echo "root" | sudo mysql_secure_installation utility
sudo systemctl start mysql
echo "root" | mysqladmin -u root -p version
sudo /etc/init.d/mysql restart