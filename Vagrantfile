# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "stshryu/steebox"
  
  config.vm.provider "virtualbox" do |v|
    v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
  end
  
  config.vm.synced_folder "../steebot", "/home/vagrant/vagrant"
end
