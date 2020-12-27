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

conda-env: ## create conda environment
	conda env create --file environment.yml

conda-requirements: ## export/update conda requirements for mac
	conda env export > environment.yml

.PHONY: build build-mac run conda-requirements conda-env
