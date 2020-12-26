build-linux:
	pyinstaller ./pyi/asciiviewer_linux.spec

build-mac:
	python -m PyInstaller \
	--onefile --windowed  --clean --noconfirm \
	./pyi/asciiviewer_mac.spec

run:
	dist/AsciiViewer

conda_env: ## create conda environment
	conda env create --file environment.yml

conda_requirements: ## export/update conda requirements for mac
	conda env export > environment.yml

.PHONY: build build-mac run conda_requirements conda_env
