# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Unreleased

## 0.9.0 - 2025-04-07

### Changed

- Drop support for Python 3.8. (Pull #85)

### Added

- Add support for `click.Command`-like, `click.Group`-like and `click.Context`-like objects without requiring them to be actual subclasses. (Pull #82)

### Fixed

- Remove explicit reference to `click.BaseCommand` and `click.MultiCommand` objects in anticipation of their deprecation. (Pull #82)
- Properly ensure whitespace is trimmed from the usage string. (Pull #83)
- Propagate `context_settings` to `click.Context`-like objects. (Pull #79)
- Allow commands with no options. (Pull #84)

## 0.8.1 - 2023-09-18

### Fixed

- `:prog_name:` and other options can now contain multiple words (it used to stop at whitespace). (Pull #60)
- `::: mkdocs-click` directive is now recognized at the end of the file without needing an extra newline. (Pull #69)
- Code blocks are marked as ```text so that HighlightJS doesn't try to highlight the "syntax" as some random language. (Pull #61)

## 0.8.0 - 2022-06-19

### Added

- Add `list_subcommands` option. (Pull #55)

## 0.7.0 - 2022-04-28

### Added

- Add `show_hidden` option. (Pull #52)
- Update package metadata. (Pull #53)

## 0.6.0 - 2022-04-02

### Changed

- Only support newer versions of `click` in response to a breaking change. (Pull #49)

## 0.5.0 - 2021-11-19

### Added

- Add ability to ignore ASCII art. (Pull #45)

### Fixed

- Correctly handle default values of `None`. (Pull #41)

## 0.4.0 - 2021-05-12

### Added

- Relax `click` version constraint. (Pull #39)

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
