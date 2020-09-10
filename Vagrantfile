# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  # install vagrant-vbguest to sync folders
  config.vagrant.plugins = "vagrant-vbguest"

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "centos/7"

  config.ssh.forward_x11 = true
  config.ssh.forward_agent = true

  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"

  config.vm.provision "shell", inline: <<-SHELL
    yum -y update
    yum install -y epel-release
    yum install -y wxPython-devel
    yum install -y xorg-x11-xauth
    curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | sudo python
    pip install pyinstaller==3.6
  SHELL
end
