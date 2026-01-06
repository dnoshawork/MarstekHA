# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] - 2026-01-06

### Added
- Initial development release of Marstek Venus E 3.0 Home Assistant integration
- UDP communication with battery on port 30000
- Support for multiple operating modes (Auto, AI, Manual, Passive)
- Real-time monitoring of battery parameters:
  - State of Charge (SOC)
  - Battery Temperature
  - Battery Voltage and Current
  - Battery Power
  - Grid Power (OnGrid Power)
  - Load Power
  - PV Power (Solar)
  - Charge Power
  - Discharge Power
- Config flow for easy setup via UI
- Automatic retry mechanism with exponential backoff (inspired by Jeedom script)
- Support for multiple time slots in Manual mode (up to 10 time periods)
- Services to control battery modes
- HACS integration support with one-click install button
- Comprehensive documentation with examples
- Version management system with bump_version.py script
- CHANGELOG following Keep a Changelog format

### Fixed
- UDP socket binding: using `("0.0.0.0", port)` to properly listen on all network interfaces
- UDP buffer size set to 65535 bytes for better compatibility with battery responses
- Improved error handling with specific error messages for different failure scenarios

### Changed
- Enhanced logging throughout the integration:
  - Debug logs for UDP requests and responses
  - Detailed error messages in config flow showing IP, port, and specific errors
  - Comprehensive error logging for socket timeouts, JSON decode errors, and OSError
- JSON formatting aligned with Jeedom reference script (compact separators)

### Notes
- ⚠️ This is a development version. The integration is functional but may require further testing and refinement
- Based on the [Jeedom script](https://github.com/dnoshawork/MarstekVenusE3.0_For_Jeedom/blob/main/marstek_udp_client_all_v3.py)

[Unreleased]: https://github.com/dnoshawork/MarstekHA/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/dnoshawork/MarstekHA/releases/tag/v0.0.1
