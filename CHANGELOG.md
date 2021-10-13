# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [3.0.1] - 2021-10-13

### Changed

-   Force xlrd dependency to less than version 2.

## [3.0.0] - 2021-09-07

### Changed

-   Changed API for maintenance module. The sched_om function has now been
    replaced with the SchedOM class.
-   Improved speed of weather window calculation.
-   Improved efficiency of log phase initialisation for O&M.
-   Improve efficiency by copying and storing sched_sol objects to check for
    matching requirements in future calls.
-   Improved WaitingTime class tests using synthesised time series.
-   Enforce requirement for fixed time step for metocean input data.

### Fixed

-   Fixed units in logging.

## [2.0.0] - 2019-03-07

### Added

-   Added warning about long waiting times.
-   Added greater logging detail to help understand reasons for failure.
-   Added combined weather window strategy that looks for the combination of
    windows which has the minimum gaps (now defined as waiting time).
-   If less than three years of metocean data is given it is now copied to
    simulate a longer time period.
-   Added transit times to maintenance operation scheduling.
-   The sched_om function now accepts a user supplied WaitingTime object using
    the optional custom_waiting argument. This allows a single WaitingTime
    object to be reused between calls.
-   Added a maximum start delay option to WaitingTime class.

### Changed

-   Removed input checks for variables which are not currently used in the code.
-   Updated warnings about operational limits.
-   Removed global variables in weather window calculation.
-   Reduced the depth of some imports for scheduling functions.
-   Tidied up port load and area requirements test for foundations installation.
-   Unified selection of burial technique function for cable lay installation
    phases.
-   Refactored port/vessel/equipment matching code to make it less obscure.
-   Changed the concept of waiting time from delays while waiting for a window
    to delays when operating over a combination of windows. These can then be
    costed at full vessel rates.
-   Moved WaitingTime class and support functions from schedule_ins module to
    schedule_shared so it can be used by the maintenance scheduling.
-   Refactored sched_om to use WaitingTime class.
-   Reimplemented waiting time costing for maintenance operations.
-   Changed maintenance port selection to use approximate distance algorithm.
-   Made setting of optimise_delay flag in WaitingTime class explicit using
    method set_optimise_delay. It can no longer be set when initialising a
    WaitingTime object.
-   OLC matching from previous weather window searches now uses a tolerance
    which is set using the match_tolerance argument to WaitingTime. It defaults
    to 0.1.
-   Changed snap_to_grid function to SnapToGrid class for reuse of expensive
    computation.
-   Now using the journey duration rather than the total duration (including 
    prep time) for weather window selection.
-   Now using the mean start delay rather than the sum of all start delays (from
    each year of metocean data) to avoid excessive values.
-   The last year of metocean data is no longer searched for an operation start
    date. This allows at least a year's data to be available for all start dates
    in the previous year.

### Fixed

-   Fixed some inconsistent definitions of vessel names.
-   Fixed matching of port terminal type.
-   Fixed bug where simulation would stop if any combination of resources could
    not find a weather window.
-   Fixed bug when only using one year of weather data.
-   Fixed bug with jacking time being overestimated.
-   Fixed issue identifying the correct connector IDs for dynamics cables
    maintenance feasibility check.
-   Caught case where OLC conditions generate no weather windows in WaitingTime
    class.
-   Improved efficiency of logOp_init function by better parsing of dataframe.
-   Fixed bug where mass and area were swapped when calculating loading
    requirements for gravity foundations.
-   Fixed bug where the device bollard pull was set to its mass rather than the
    user provided quantity.
-   Fixed bug where the weather window containing the start time would not be
    selected even if there is enough remaining time to complete the operation.
-   Fixed issue with gravity foundations not being included in the installation
    plan.
-   The substation pile no longer requires an anchor to be fitted and the
    substation is installed after the pile.
-   Ensured that the waiting time lists are summed when doing comparisons for
    finding the optimal solution.
-   Fix bug with number of mattresses and rock bags being floats rather than ints.
-   Fix example plotting bugs.

## [1.0.0] - 2017-01-05

### Added

-   Initial import of dtocean-logistics from SETIS.
