build:
	cd asciiviewer && \
	pyinstaller AsciiViewer.spec

build-mac:
	cd asciiviewer && \
	python -m PyInstaller \
	--onefile --windowed  --clean --noconfirm \
	./AsciiViewerMac.spec

run:
	asciiviewer/dist/AsciiViewer

conda_env: ## create conda environment
	conda env create --file environment.yml

conda_requirements: ## export/update conda requirements for mac
	conda env export > environment.yml

.PHONY: build build-mac run conda_requirements conda_env
