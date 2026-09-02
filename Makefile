.DEFAULT_GOAL := help

VERSION = 0.4.0
ENV_NAME = asciiviewer

.PHONY: help
help: ## this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_0-9-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: conda-env
conda-env: ## create the conda environment if it doesn't already exist
	@conda env list | grep -qE "^$(ENV_NAME)[[:space:]]" || conda env create -f environment.yml

.PHONY: build-linux
build-linux: conda-env ## build on linux
	conda run --no-capture-output -n $(ENV_NAME) pyinstaller --dist ./dist/linux --clean --noconfirm ./asciiviewer.spec

.PHONY: build-mac
build-mac: conda-env ## build on macos
	conda run --no-capture-output -n $(ENV_NAME) pyinstaller --dist ./dist/macos --clean --noconfirm ./asciiviewer.spec

.PHONY: build-spec
build-spec: conda-env ## build spec file for pyinstaller
	conda run --no-capture-output -n $(ENV_NAME) pyi-makespec \
	--onedir --windowed --noupx \
	--name asciiviewer-raw \
	--path ./ \
	--add-data="./asciiviewer/assets/splash.png:assets" \
	--add-data="./asciiviewer/assets/default.cfg:assets" \
	--add-data="./asciiviewer/examples/fmap:examples" \
	--add-data="./asciiviewer/examples/MCOMPO_UOX_TBH:examples" \
	--add-data="./asciiviewer/examples/BurnupV3:examples" \
	--add-data="./asciiviewer/examples/MultiCompoV4:examples" \
	--add-data="./asciiviewer/examples/XsmFuelMapV4:examples" \
	--add-data="./asciiviewer/examples/XsmMultiCompoV4:examples" \
	--log-level DEBUG \
	--debug all \
	--icon "./asciiviewer/assets/icon.ico" \
	./asciiviewer/main.py

.PHONY: format
format: conda-env ## format the codebase with ruff
	conda run --no-capture-output -n $(ENV_NAME) ruff format .

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
	python -m build
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
