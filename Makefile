build-linux:
	python -m PyInstaller \
	--dist ./dist/linux \
	--onefile --windowed  --clean --noconfirm \
	./asciiviewer.spec

build-windows:
	python -m PyInstaller \
	--onefile --windowed --clean --noconfirm --noupx \
	--dist ./dist/windows --name asciiviewer \
	--path ./asciiviewer/source \
	--add-data="asciiviewer\splash.jpg;." \
	--add-data="asciiviewer\default.cfg;." \
	--add-data=".\asciiviewer\example\fmap;example" \
	--add-data=".\asciiviewer\example\MCOMPO_UOX_TBH;example" \
	--log-level DEBUG \
	--debug all \
	./asciiviewer/AsciiViewer.py

build-windows-spec:
	python -m PyInstaller \
	--dist ./dist/windows \
	--onefile --windowed --noconsole --clean --noconfirm --noupx \
	./asciiviewer.spec

build-mac:
	python -m PyInstaller \
	--onefile --windowed  --clean --noconfirm \
	./asciiviewer.spec

centos7-up:
	vagrant up centos7

centos7-ssh:
	vagrant ssh centos7

conda-env: ## create conda environment
	conda env create --file environment.yml

conda-requirements: ## export/update conda requirements for mac
	conda env export > environment.yml

docker-win-py3:
	docker run -it --rm -v "$$(pwd):/src/" \
	--entrypoint /bin/sh cdrx/pyinstaller-windows:python3-32bit \
	-c "apt-get install make && pip install -r requirements.txt && /bin/bash"

docker-py2:
	docker run -it --rm -v "$$(pwd):/src/" \
	--entrypoint /bin/sh cdrx/pyinstaller-linux:python2 -c /bin/bash

docker-py3:
	docker run -it --rm -v "$$(pwd):/src/" \
	--entrypoint /bin/sh cdrx/pyinstaller-linux:python3 -c /bin/bash

.PHONY: build build-mac run conda-requirements conda-env centos7-up centos7-ssh
