.DEFAULT_GOAL := help

VERSION = 0.2.0-dev0

.PHONY: help
help: ## this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_0-9-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: build-linux
build-linux: ## build on linux
	python -m PyInstaller --dist ./dist/linux --clean --noconfirm ./asciiviewer.spec

.PHONY: build-mac
build-mac: ## build on macos
	python -m PyInstaller --dist ./dist/macos --clean --noconfirm ./asciiviewer.spec

.PHONY: build-wine
build-wine: ## build on wine
	python -m PyInstaller --dist ./dist/windows --clean --noconfirm ./asciiviewer.spec

.PHONY: docker-wine
docker-wine: ## run docker to build windows binary with wine and python3
	docker run -it --rm -v "$$(pwd):/src/" \
	--entrypoint /bin/sh cdrx/pyinstaller-windows:python3-32bit \
	-c "apt-get install -y make && pip install -r wine-requirements.txt && make build-wine && /bin/bash"

.PHONY: build-spec
build-spec: ## build spec file for pyinstaller
	pyi-makespec \
	--onedir --windowed --noupx \
	--name asciiviewer-raw \
	--path ./ \
	--add-data="./asciiviewer/assets/splash.png:assets" \
	--add-data="./asciiviewer/assets/default.cfg:assets" \
	--add-data="./asciiviewer/examples/fmap:examples" \
	--add-data="./asciiviewer/examples/MCOMPO_UOX_TBH:examples" \
	--log-level DEBUG \
	--debug all \
	--icon "./asciiviewer/assets/icon.ico"
	./asciiviewer/main.py

.PHONY: centos-up
centos-up: ## start centos7
	vagrant up centos7

.PHONY: centos-ssh
centos-ssh: ## ssh into centos7
	vagrant ssh centos7

.PHONY: conda-env
conda-env: ## create conda environment
	conda env create --file environment.yml

.PHONY: conda-requirements
conda-requirements: ## export/update conda requirements
	conda env export > environment.yml

.PHONY: create-git-tag
create-git-tag: ## create git tag
	git tag -a v$(VERSION) -m "v$(VERSION)"

.PHONY: push-git-tag
push-git-tag: ## push git tag to origin
	git push origin v$(VERSION)

.PHONY: delete-git-tag
delete-git-tag: ## delete local and remote git tags
	-git tag -d v$(VERSION)
	-git push --delete origin v$(VERSION)

.PHONY: tag
tag: delete-git-tag create-git-tag push-git-tag

.PHONY: dist
dist: ## create *.whl and *.tar.gz distributions
	python3 setup.py bdist_wheel sdist
	-tar xvzf dist/*.tar.gz -C dist
	-unzip dist/*.whl -d dist/whl

.PHONY: clean
clean: ## remove all build and python artifacts
clean: clean-build clean-pyc

.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
