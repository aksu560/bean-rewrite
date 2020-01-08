#!/usr/bin/env bash

sudo apt-get install -y vim curl python-software-properties
sudo apt-get update
sudo apt-get -y install mysql-server
sudo systemctl start mysql
echo "root" | mysqladmin -u root -p version
sudo /etc/init.d/mysql restart