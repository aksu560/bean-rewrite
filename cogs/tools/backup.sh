#!/bin/bash

cd /vagrant
mkdir -p db_backup
sudo -u postgres pg_dump beanbase > db_backup/beanbase.tar
cd db_backup
mv beanbase.tar beanbase-$(date '+%Y%m%d%H%M').tar