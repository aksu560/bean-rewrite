#!/usr/bin/env bash

debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
apt-get update
apt-get install -y mysql-server
sudo systemctl start mysql
sudo /etc/init.d/mysql restart

mysql-uroot -uroot -proot -e "CREATE DATABASE IF NOT EXISTS bot"
mysql-uroot -uroot -proot -e "grant all privileges on bot.* to 'bean' identified by 'root'"