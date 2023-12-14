# Changelog

All notable changes to `gstat_exporter` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- Added argparse and commandline arguments -p and -l to make listen ip and listen port configurable
- Added feature to remove devices when they disappear from the system
- Added -d / --debug flag to enable debug mode

### Changed
- Replace black + flake8 linters with ruff
- Refactor code into a GstatExporter class
- Made the gstat sleep period configurable with -s / --sleep and change the default from 5 secs to 15 secs (the default scrape interval in Prometheus)
- Add timestamp and configure logformat so it now looks like this:
    "2023-12-14 13-26-14 +0100 - gstat_exporter - LEVEL - message"


## [v0.1.0] - 2023-12-13

### Changed
- Create Python package
- Rename default branch from "master" to "main"


### Added

- CHANGELOG.md
- RELEASE.md
