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

conda_requirements: ## export/update conda requirements for mac
	conda env export > requirements_mac.yml

.PHONY: build build-mac run conda_requirements
