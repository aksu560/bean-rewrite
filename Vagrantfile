# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  config.vm.box = "hashicorp/bionic64"
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"
  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    end
  config.vm.provision "shell",
    path: "provision/mysql.sh"
  config.vm.provision "shell",
    path: "provision/python.sh"
  config.vm.provision "shell",
    path: "provision/launch.sh"

end
