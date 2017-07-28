# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- Added warning about long waiting times.
- Add README and CHANGELOG
- Add continuous integration setup files.
- Added greater logging detail to help understand reasons for failure.

### Changed

- Removed input checks for variables which are not currently used in the code.
- Updated warnings about operational limits.
- Weather window calculation (installation) rewritten to remove global
  variables.
- Reduced the depth of some imports for scheduling functions.
- Tidied up port load and area requirement test for foundations installation.
- Unified selection of burial tecnhnique function for cable lay installation
  phases.
- Refactored port/vessel/equipment matching code to make it less obscure.

### Fixed

- Fixed some incosistent definitions of vessel names.
- Fixed matching of port terminal type
- Fixed bug where simulation would stop if any combination of resources could
  not find a weather window.
- Fixed bug when only using one year of weather data

### Removed

- Removed waiting times from cost calculation due to long potential waits.

## [1.0.0] - 2017-01-05

### Added

- Initial import of dtocean-logistics from SETIS.


