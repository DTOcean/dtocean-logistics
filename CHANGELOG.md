# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- Added warning about long waiting times.
- Added greater logging detail to help understand reasons for failure.
- Added combined weather window strategy that looks for the combination of
  windows which has the minimum gaps (now classed as waiting time).
- Added transit times to maintenance operation scheduling.
- The sched_om function now accepts a user supplied WaitingTime object using
  the optional custom_waiting argument. This allows a single WaitingTime
  object to be reused between calls.

### Changed

- Removed input checks for variables which are not currently used in the code.
- Updated warnings about operational limits.
- Weather window calculation (installation) rewritten to remove global
  variables.
- Reduced the depth of some imports for scheduling functions.
- Tidied up port load and area requirement test for foundations installation.
- Unified selection of burial technique function for cable lay installation
  phases.
- Refactored port/vessel/equipment matching code to make it less obscure.
- Changed the concept of waiting time from delays while waiting for a window
  to delays when operating over a combination of windows. These can then be
  costed at full vessel rates.
- Moved WaitingTime class and support functions from schedule_ins module to
  schedule_shared so it can be used by the maintenance scheduling.
- Refactored sched_om to use WaitingTime class.
- Reimplemented waiting time costing for maintenance operations.
- Changed maintenance port selection to use approximate distance algorithm.
- Made setting of optimise_delay flag in WaitingTime class explicit using
  method set_optimise_delay. It can no longer be set when initialising a
  WaitingTime object.
- OLC matching from previous weather window searches now uses a tolerance
  which is set using the match_tolerance argument to WaitingTime. It defaults
  to 0.1.
  

### Fixed

- Fixed some inconsistent definitions of vessel names.
- Fixed matching of port terminal type
- Fixed bug where simulation would stop if any combination of resources could
  not find a weather window.
- Fixed bug when only using one year of weather data.
- Fixed bug with jacking time being overestimated.
- Fixed issue identifying the correct connector IDs for dynamics cables
  maintenance feasibility check.
- Catch case where OLC conditions generate no weather windows in WaitingTime
  class.
- Improved efficiency of logOp_init function by better parsing of dataframe.

## [1.0.0] - 2017-01-05

### Added

- Initial import of dtocean-logistics from SETIS.


