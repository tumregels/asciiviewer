build7:
	pyinstaller ./pyi/asciiviewer_centos7.spec

build6:
	pyinstaller --clean --noconfirm --onefile -n asciiviewer \
	./pyi/asciiviewer_centos6.spec

build-mac:
	python -m PyInstaller --onefile --windowed  --clean --noconfirm \
	./pyi/asciiviewer_macos.spec

run:
	dist/asciiviewer

centos6_up:
	-VAGRANT_VAGRANTFILE=vagrant/Vagrantfile_centos_6 vagrant up

centos6_ssh:
	-VAGRANT_VAGRANTFILE=vagrant/Vagrantfile_centos_6 vagrant ssh

conda_requirements: ## export/update conda requirements for mac
	conda env export > requirements_mac.yml

.PHONY: build6 build7 build-mac run centos6_up centos6_ssh conda_requirements
