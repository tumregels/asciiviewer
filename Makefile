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

.PHONY: build run
