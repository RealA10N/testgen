# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2] - 16.06.2022

### Added

- Added the abstract `validate` function to test cases.
- Collected test generating functions that contain `_` in their name are now replaced with `-`.
- The `write_answer` function now can read the input file, provided as a parameter.

### Changed

- Renamed `write_in` and `write_ans` functions to `write_input` and `write_answer`, respectively.

[v0.2]: https://github.com/RealA10N/testgen/compare/v0.1...v0.2
