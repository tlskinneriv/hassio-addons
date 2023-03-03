# Changelog

All notable changes to this project will be documented in this file.

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
