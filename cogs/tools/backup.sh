#!/bin/bash

cd /vagrant
mkdir -p db_backup
sudo -u postgres pg_dump beanbase > db_backup/beanbase.vak
cd db_backup
mv beanbase.bak beanbase-$(date '+%Y%m%d%H%M').bak