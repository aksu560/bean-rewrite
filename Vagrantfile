# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|


  config.vm.box = "ubuntu/bionic64"

  config.vm.synced_folder './', '/vagrant', type: 'nfs'
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.provision "shell",
    path: "provision/mysql.sh"
  config.vm.provision "shell",
    path: "provision/python.sh"
  config.vm.provision "shell",
    path: "provision/launch.sh"

end
