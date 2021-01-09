# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "centos7" do |config|
    config.vm.box = "centos/7"
    config.vagrant.plugins = {"vagrant-vbguest" => {"version" => "0.21.0"}}
    config.ssh.forward_x11 = true
    config.ssh.forward_agent = true
    config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
    config.vm.provision "shell", privileged: false, inline: <<-SHELL
      sudo yum -y update
      sudo yum -y install gtk3-devel
      if [ ! -d ~/miniconda3 ]; then
        mkdir -p ~/miniconda3
        curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o ~/miniconda3/miniconda.sh
        bash ~/miniconda3/miniconda.sh -b -u -f -p ~/miniconda3
        rm -rf ~/miniconda3/miniconda.sh
      fi
      ~/miniconda3/bin/conda env create --file /vagrant/environment.yml
      cd /vagrant && \
      ~/miniconda3/envs/asciiviewer/bin/pyinstaller --clean -y --dist ./dist/linux/centos7 --workpath /tmp \
      ./asciiviewer.spec
    SHELL
  end

  config.vm.define "ubuntu" do |config|
    config.vm.box = "ubuntu/trusty64"
    config.vm.box_version = "20190514.0.0"
    config.vm.provision "shell", privileged: false, inline: <<-SHELL
      sudo apt-get -y update
      if [ ! -d ~/miniconda3 ]; then
        mkdir -p ~/miniconda3
        curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o ~/miniconda3/miniconda.sh
        bash ~/miniconda3/miniconda.sh -b -u -f -p ~/miniconda3
        rm -rf ~/miniconda3/miniconda.sh
      fi
    SHELL
  end

  config.vm.define "sierra" do |config|
    config.ssh.forward_x11 = true
    config.ssh.forward_agent = true
    config.vm.synced_folder ".", "/vagrant", type: 'rsync'
    config.vm.box = "jhcook/macos-sierra"
    config.vm.box_version = "10.12.6"
    config.vm.provider "virtualbox" do |vb|
      vb.customize ["modifyvm", :id, "--usb", "on"]
      vb.customize ["modifyvm", :id, "--usbehci", "off"]
    end
  end

end
