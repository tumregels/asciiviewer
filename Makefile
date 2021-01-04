build-linux:
	python -m PyInstaller \
	--onefile --windowed  --clean --noconfirm \
	./pyi/asciiviewer_linux.spec

build-mac:
	python -m PyInstaller \
	--onefile --windowed  --clean --noconfirm \
	./pyi/asciiviewer_mac.spec

run:
	dist/asciiviewer

centos7-up:
	vagrant up centos7

centos7-ssh:
	vagrant ssh centos7

conda-env: ## create conda environment
	conda env create --file environment.yml

conda-requirements: ## export/update conda requirements for mac
	conda env export > environment.yml

.PHONY: build build-mac run conda-requirements conda-env centos7-up centos7-ssh
