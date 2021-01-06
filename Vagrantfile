# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "centos7" do |centos7|
    centos7.vm.box = "centos/7"
    centos7.vagrant.plugins = {"vagrant-vbguest" => {"version" => "0.21.0"}}
    centos7.ssh.forward_x11 = true
    centos7.ssh.forward_agent = true
    centos7.vm.synced_folder ".", "/vagrant", type: "virtualbox"
    centos7.vm.provision "shell", privileged: false, inline: <<-SHELL
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

end
