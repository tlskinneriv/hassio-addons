# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2024-03-30

### Changed

- Update logging format to include file name and line number for easier troubleshooting; update format for readability.
- Update logger for WSGI to use the built-in Python logger (and not log out to stderr, thanks @jruby411!).

## [1.1.0] - 2024-01-27

### Changed

- Add MAC address override option to add-on. Add the MAC address of the device in the option to
  override the PASSKEY data.

## [1.0.1] - 2023-09-09

### Changed

- Update the way that malformed requests are handled: instead of assuming that the data will be
  parsed into the headers, look for the broken request string and reassemble it. Limit to 3 lines of
  lookahead to prevent server blocking if the request is highly malformed.
- HOUSEKEEPING: Updated base container to python3.11/alpine3.18.
- HOUSEKEEPING: Updated devcontainer config to be compliant with current VS Code recommendations.

## [1.0.0] - 2023-03-02

### Added

- Add support for building all architectures

### Changed

- Change path of awnet files

### Housekeeping

- Update devcontainer to use root, add extensions
- GitHub actions
- config.json and repository.json -> yaml

## [0.1.2] - 2022-08-03

### Added

- More debug logs
- Helpful error message if query string is missing
- Log level option to the configuration, default is WARNING

### Fixed

- Updated handling of the request to return 400 on requests with no query string
- Updated handling of the request to support the malformed HTTP request from WS-5000 devices. Closes #7.

## [0.1.1] - 2022-05-22

- Add `"init": false` to `config.json` to resolve issues with the s6 overlay issue. Closes #5.
- Updates the documentation to be more clear about add-on setup and configuration of the Ambient Weather device.

## [0.1.0] - 2022-01-01

- Initial release of this project
