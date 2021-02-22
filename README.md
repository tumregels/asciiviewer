<h1 align="center">
<img src="images/logo.png" alt="asciiviewer logo" width="400px" />

![Build](https://github.com/tumregels/asciiviewer/workflows/Build/badge.svg?branch=master)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

</h1>

<h5 align="center">A pretty viewer for XSM files generated by DRAGON/DONJON or APOLLO neutronic codes</h1>

<div align="center">
<img src="images/preview.png" alt="asciiviewer preview" width="700" />
</div>

## Demo

<details>
<summary>Linux</summary>
<div align="center">
<img src="https://raw.github.com/tumregels/asciiviewer/master/images/linux.gif?raw=true" alt="linux demo" width="700" />
</div>
</details>

<details open>
<summary>Windows</summary>
<div align="center">
<img src="https://raw.github.com/tumregels/asciiviewer/master/images/windows.gif?raw=true" alt="windows demo" width="700" />
</div>
</details>

<details>
<summary>MacOS</summary>
<div align="center">
<img src="https://raw.github.com/tumregels/asciiviewer/master/images/macos.gif?raw=true" alt="macos demo" width="700" />
</div>
</details>

## About

As a DRAGON/DONJON user, you want to look inside a `LCM` object, such as
`LINKED_LIST`, `SEQ_ASCII` or `XSM_FILE`.
The simplest way to do this is to convert your object into `XSM_FILE` or `SEQ_ASCII` format

    SEQ_ASCII mySeqFile ; mySeqFile := myLCMObject ;

perform calculation and open the resulting output file with __asciiviewer__.

The initial version of __asciiviewer__ was written by Benjamin Toueg in 2009
and is available [here](http://code.google.com/p/dragon-donjon-ascii-viewer/).

Here, the original source code was ported to run on both python 2 and 3 with [wxpython 4](https://www.wxpython.org/).
Single file executables are generated with [pyinstaller](https://www.pyinstaller.org/) using [these workflows](.github/workflows)
via [github actions](https://github.com/tumregels/asciiviewer/actions).

## Installation

The easiest way to run __asciiviewer__
is to download the executable from [releases](https://github.com/tumregels/asciiviewer/releases/latest)
as shown in the [demo](#demo).
Otherwise set it up [manually](#manual-setup).

### Manual setup

First step is to install [miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
which requires no admin priviledges.

Clone or [download](https://github.com/tumregels/asciiviewer/archive/master.zip) the __asciiviewer__ project

    $ git clone https://github.com/tumregels/asciiviewer

Open a new terminal and create conda environment

    $ cd asciiviewer
    $ conda env create -f environment.yml

Activate the conda environment and run `asciiviewer` command

    $ source activate asciiviewer
    (asciiviewer) $ asciiviewer

or

    (asciiviewer) $ python asciiviewer/main.py

on MacOS you need to use `pythonw`

    (asciiviewer) $ pythonw asciiviewer/main.py

To open a specific DRAGON/DONJON output file from the command line

    (asciiviewer) $ asciiviewer ./path/to/file

To generate the single file executable on your computer

    (asciiviewer) $ pyinstaller --clean --noconfirm ./asciiviewer.spec

The above step will create an executable under the `dist` folder.

__Important__ - single file executables can be called from terminal with or without file path

    $ ./asciiviewer ./path/to/file

### Dev setup

For development setup first implement the [manual setup](#manual-setup) followed by

    (asciiviewer) $ python -m pip install -r requirements-dev.txt

To get a detailed traceback set [`PYTHONFAULTHANDLER`](https://docs.python.org/dev/using/cmdline.html#envvar-PYTHONFAULTHANDLER). On MacOS and Linux

    (asciiviewer) $ export PYTHONFAULTHANDLER=1

To release a new version execute

    (asciiviewer) $ bump2version minor

Above command will update the minor release version, create a git tag and a commit.
Now push the git tag and the commit with

    (asciiviewer) $ git push --follow-tags

### Configuration

On the first run __asciiviewer__ will create an `.asciiviewer.cfg` config file at
`HOME` directory with [this content](./asciiviewer/assets/default.cfg).
From this file you can disable sort and splash screen.

## Issues

Any problems or bugs should be reported [here](https://github.com/tumregels/asciiviewer/issues)

### Known issues

* The __asciiviewer__ executables are not signed and you will get warnings on MacOS and Windows.

* The program may crash unexpectedly when used with big files.

* On ubuntu, during manual setup you may get `missing libgtk-x11-2.0.so.0` error.
  One solution is to reinstall `libgtk2.0` library

      $ sudo apt-get install --reinstall libgtk2.0-0
