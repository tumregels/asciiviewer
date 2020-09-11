build:
	cd asciiviewer && pyinstaller AsciiViewer.spec

run:
	asciiviewer/dist/AsciiViewer

.PHONY: build run
