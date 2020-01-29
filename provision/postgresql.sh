sudo apt-get install -y postgresql postgresql-contrib
sudo update-rc.d postgresql enable
sudo service postgresql start
sudo apt-get install libpq-dev

sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'root';"

