#!/usr/bin/env bash

debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
sudo apt-get update
sudo apt-get install -y mysql-server
sudo apt-get install
sudo systemctl start mysql
sudo /etc/init.d/mysql restart
sudo apt-get install libmysqlclient-dev
pip3 install mysqlclient
pip3 install sqlalchemy_utils