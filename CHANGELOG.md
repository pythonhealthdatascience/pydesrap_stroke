# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Dates formatted as YYYY-MM-DD as per [ISO standard](https://www.iso.org/iso-8601-date-and-time-format.html).

## v1.0.0 - 2026-02-11

Stable release, with minor changes from 0.2.0 including quality assurance documentation, bash script simplification, and security and bug fixes.

### Added

* Add `docs/quality_assurance.md`.

### Changed

* Simplified `run_notebooks.sh`.

### Fixed

* Upgraded packages to address security risks identified by GitHub Dependabot:
    * `nbconvert` (7.16.6 to 7.17.0).
    * `pip` (25.0 to 26.0.1).
    * `jinja2` (3.1.5 to 3.1.6).
* Upgraded `genbadge` (`pkg_resources` warning with 1.1.2 - upgraded to 1.1.3).

## v0.2.0 - 2025-11-06

This release has some small additions (e.g., data dictionary, coverage), alongside lots of refactoring and changes (e.g., parameters in JSON, using `DistributionRegistry`, renaming repository, using updated version of `sim-tools`).

### Added

* Data dictionary.
* Add coverage badge (requiring `pytest-cov` and `genbadge` to be add to environment).
* Add option to choose between operating system and coverage when run tests via GitHub actions.
* Add tests for `LockedDict`.

### Changed

* Refactored to used `parameters.json` and `sim-tools.DistributionRegistry()`, and fixed analysis and tests etc. to work with this new set-up.
* Renamed (`stroke_rap_python` -> `pydesrap_stroke`, `rap_template_python_des` -> `pydesrap_mms`).
* README - add DOI, contributors, licence, funding, and generally improved.
* STRESS-DES - rewrote/improved answers.
* Environment - renamed environment, and upgraded kaleido and sim-tools.
* Removed `tia_esd` from parameters and csv (as upgraded sim-tools no longer allows it).
* Updated `Discrete` to `DiscreteEmpiricial` (as updated sim-tools name)
* Updated pyproject.toml (non-dynamic description, author list).
* Other minor corrections/changes (e.g. moving `RestrictAttributes`, docstring corrections).

### Fixed

* Fixed `run_notebooks.sh`.
* Blocked dot notation for `LockedDict`.

## v0.1.0 - 2025-06-02

🌱 First release of the repository. Contains implementation of the DES model from Monks et al. 2016, with reproduction of all tables and figures with results from the article and supplementary material. Also includes some tests, and a demonstration of logging, and of how parameters could be stored in a `.csv`.