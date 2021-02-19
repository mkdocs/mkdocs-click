# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 0.3.0 - 2021-02-19

### Changed

- `--help` is now kept in options (it used to be automatically dropped). (Pull #29)

### Added

- Add table formatting. (Pulls #25, #30)
- Use `:prog_name:` more consistently in usage. (Pull #24)
- Allow using full command paths in headers. (Pull #36)

### Fixed

- Make usage and options headings bold to improve legibility. (Pull #31)

## 0.2.0 - 2020-12-09

### Added

- Add `:prog_name:` option to allow overriding the name of the CLI program. (Pull #8, contributed by @frankier.)
- Add official support for Python 3.9. (Pull #20)

### Fixed

- Properly pin `click==7.*` and `markdown==3.*`. (Pull #19)

## 0.1.1 - 2020-06-05

### Fixed

- Raise proper error when processing unnamed commands. (Pull #4)

## 0.1.0 - 2020-06-04

_Initial implementation._

### Added

- Add `::: mkdocs-click` block with `:module:`, `:command:` and `:depth:` options.
