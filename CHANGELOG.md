# Changelog

## [0.3.0] - 2026-07-27

### Fixed
- Segfault when opening a second file after viewing a table
- `wxPython` 4.2.5 sizer assertion crash; bumped minimum wxPython requirement
- Crash opening real XSM binary files
- `TypeError` crash in the filter panel's `GridSizer`

### Changed
- Removed Python 2 support from the codebase
- Removed the unused CERN ROOT dependency
- Removed stray comment lines from the code
- Updated the About dialog
- Added example cases

### Packaging & CI
- Replaced `pbr`/`bump2version` packaging with `uv`, then later removed `uv` entirely in favor of conda
- Switched CI to Miniconda and dropped uv-specific packaging config
- Modernized GitHub Actions and dropped the Wine cross-build
- Bumped GitHub Actions versions to clear Node.js 20 deprecation warnings
- Added OS labels to builds/releases and updated the Makefile

## [0.2.0] - 2021-02-22

### Added
- Application icon and logo
- Application versioning logic

### Fixed
- Corner-case exception when navigating back to the root of the tree

### Changed
- Disabled the incomplete search functionality
- Updated the app exit logic and removed the close button
- Ignored deprecation warnings in frozen (packaged) builds
- Minor cleanup and module renaming (dropped `me_` prefixes)
- Reorganized application/package structure and paths

### Packaging & CI
- Removed the Wine release workflow
- Reorganized the Makefile and cleaned up workflow files

## [0.1.0] - 2021-01-23

### Added
- Core ASCII/XSM file viewer application
- Python 2 and 3 compatibility
- PyInstaller-based packaging with spec files for Windows, macOS, and Linux
- Conda environment and build tooling (Vagrantfile, Makefile)
- GitHub Actions workflows for Windows, macOS, and Linux builds, including a Wine-based cross-build for Windows
- Example files bundled with the binary

### Fixed
- Deprecation warnings and `wx.TreeItemData` usage for compatibility with newer wxPython versions
- Various relative path and workflow issues in the build/release pipeline
