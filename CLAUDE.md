# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

__asciiviewer__ is a desktop GUI (wxPython) for browsing `XSM_FILE` / `SEQ_ASCII` output files produced by the
DRAGON/DONJON and APOLLO neutronic codes. It parses these binary/ASCII nuclear-physics data files into a tree of
linked-list elements and lets the user navigate them in a tree view + spreadsheet-like grid, with filtering and
find. The original code was written by Benjamin Toueg in 2009 (Python 2, wx); this fork ports it to
Python 3 / wxPython 4 and packages it with PyInstaller for Windows/macOS/Linux single-file executables.

There are no automated tests in this repository — verification is manual, by running the app against the example
files under `asciiviewer/examples/`.

## Dev environment

Development relies on a conda environment (wxPython has native deps that pip alone won't reliably resolve on all
platforms):

```bash
conda env create -f environment.yml                             # one-time, creates the `asciiviewer` env
```

## Common commands

```bash
conda run -n asciiviewer asciiviewer                            # run the app
conda run -n asciiviewer python asciiviewer/main.py             # equivalent, run from source
conda run -n asciiviewer asciiviewer ./path/to/file             # open a specific DRAGON/DONJON output file

make lint                                                       # ruff check .
make lint-imports                                               # ruff check --select I .  (import sort only)
make format                                                     # ruff format .

conda run -n asciiviewer pyinstaller --clean --noconfirm ./asciiviewer.spec   # build a single-file executable into ./dist
make build-mac / make build-linux                                             # same, via conda run, output to ./dist/<platform>

conda run -n asciiviewer bump2version minor                     # bump minor version, creates a commit + git tag (see release flow below)
git push --follow-tags
```

Ruff config lives in `pyproject.toml`: line length 120, import sorting enabled (`I`), `UP031` (percent-formatting)
and `BLE001` (blind `except Exception`) are deliberately ignored — this codebase uses `%`-formatting in places and
intentionally catches broad exceptions in a few spots to keep the wx UI from crashing on bad input files.

Set `PYTHONFAULTHANDLER=1` when debugging native/wx crashes (segfaults) for a C-level traceback.

## Release flow

Version is single-sourced in `asciiviewer/_version.py` and mirrored into `Makefile`'s `VERSION` var via
`.bumpversion.cfg`. `bump2version {major,minor,patch}` updates both files, commits, and tags; then
`git push --follow-tags`. CI (`.github/workflows/release.yml`) builds platform executables from the tag.

## Architecture

**Parsing layer** (`asciiviewer/parser/`) — turns a DRAGON/DONJON file into a flat list of
`LinkedListElement(id, level, labelType, label, contentType, content)` objects (a serialized tree, `level`
encodes depth):
- `parser_tool.elementListFromFile(filePath)` sniffs the file (`$XSM` magic bytes vs. plain ASCII) and dispatches
  to the right parser. Also defines `LinkedListElement` and `Content` (a lazy wrapper — large content blocks are
  only decoded via `.getContent()` when actually needed, since files can be large).
- `ascii_parser.py` parses `SEQ_ASCII`-format files, with separate branches for the "Version3" and "Version4"
  (`->...<-`-delimited) text formats.
- `xsm_parser.py` parses the binary `$XSM` format — a direct-access, fixed-record-length database structure
  ported from the original Fortran77/C GANLIB implementation (see the module docstring for the on-disk layout).

**UI layer** (`asciiviewer/*.py`, not `parser/`) — classic wx three-pane app wired together in `main.py`:
- `MainWindow` (`main.py`) is the wx.Frame: builds a `wx.SplitterWindow` with `MyTreeCtrl` on the left and a
  `MyFilterPanel` + `MySheet` grid stacked on the right, wires menu/keyboard events, and owns the find/replace
  flow (`MyFindReplaceDialog`).
- `MyTreeCtrl` (`tree_ctrl.py`) loads the parsed `LinkedListElement` list into a `wx.TreeCtrl`, lazily resolves
  `Content` into concrete data on selection, and implements search (`find`) and derived-calculation triggers
  (e.g. computing reaction rates or multicompo calculations on demand when a `GROUP`/`CALCULATIONS` node is
  first expanded — see the `elif` chain in `MainWindow.OnSelChanged`, which is the central dispatch for "what to
  show when a tree node is selected").
- `calculation.py` / `ref_case.py` model domain-specific derived views (`MyCalculation`, `MyMicroLib`,
  `MyRefcase`) — cross-section (XS) data keyed by isotope/energy group, with filtering support.
- `table.py` defines the `wx.grid.GridTableBase` subclasses (`MySummaryTable`, `MyTableColumn`,
  `MyCalculationTable`) that back `MySheet` (`sheet.py`, a `wx.grid.Grid` subclass) — these are the adapters
  between parsed/derived data and the spreadsheet display.
- `filter_panel.py` provides the combo-box filter UI (e.g. filter by cross-section name) used by calculations
  and ref-cases; `menu_bar.py` defines menu IDs/layout.

Data flow for a typical interaction: file → `parser_tool.elementListFromFile` → `LinkedListElement` tree →
`MyTreeCtrl` → on selection, `MainWindow.OnSelChanged` resolves/derives content (`calculation.py`/`ref_case.py`
as needed) → wraps it in a `table.py` Grid table → renders in `MySheet`.

Packaging (`asciiviewer.spec`) bundles `asciiviewer/assets/*` and `asciiviewer/examples/*` as PyInstaller data
files; `application_path` in `main.py`/`__init__.py` resolves correctly both when run from source and when
frozen via `sys._MEIPASS`.

On first run the app writes `~/.asciiviewer.cfg` (from `asciiviewer/assets/default.cfg`), which stores the last
opened file path and toggles for splash screen / sort.
