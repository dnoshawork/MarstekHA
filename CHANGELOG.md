# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] - 2026-01-06

### Added

### Changed

### Fixed

### Removed


## [1.1.0] - 2026-01-06

### Fixed
- Fixed UDP socket binding issue: changed from `("", port)` to `("0.0.0.0", port)` to properly listen on all network interfaces
- UDP buffer size increased from 4096 to 65535 bytes for better compatibility
- Improved error handling with specific error messages for different failure scenarios

### Changed
- Improved logging throughout the integration:
  - Added debug logs for UDP requests and responses
  - Enhanced error messages in config flow to show IP, port, and specific error details
  - Added detailed error logging for socket timeouts, JSON decode errors, and OSError
- Aligned JSON formatting with Jeedom reference script (compact separators)

### Added
- Comprehensive changelog for version tracking
- VERSION file for easier version management
- Better documentation of UDP communication errors

## [1.0.0] - 2026-01-05

### Added
- Initial release of Marstek Venus E 3.0 Home Assistant integration
- UDP communication with battery on port 30000
- Support for multiple operating modes (Auto, AI, Manual, Passive)
- Real-time monitoring of battery parameters:
  - State of Charge (SOC)
  - Temperature
  - Voltage and Current
  - Battery Power
  - Grid Power
  - Load Power
  - PV Power
  - Charge/Discharge Power
- Config flow for easy setup via UI
- Automatic retry mechanism with exponential backoff
- Support for multiple time slots in Manual mode
- Services to control battery modes:
  - `set_battery_mode_auto`
  - `set_battery_mode_ai`
  - `set_battery_mode_manual`
  - `set_battery_mode_passive`
- HACS integration support

[Unreleased]: https://github.com/dnoshawork/MarstekHA/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/dnoshawork/MarstekHA/compare/v1.1.0...v0.0.1
[1.1.0]: https://github.com/dnoshawork/MarstekHA/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/dnoshawork/MarstekHA/releases/tag/v1.0.0
