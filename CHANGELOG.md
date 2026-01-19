# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure for LVGL MicroPython v8 with ulab for ESP32-S3
- Build system with Makefile and Python build script
- Support for three ESP32-S3 variants:
  - Generic (no PSRAM)
  - SPIRAM (standard PSRAM)
  - SPIRAM_OCT (octal PSRAM)
- Comprehensive documentation:
  - README.md with quick start guide
  - BUILD.md with detailed build instructions
  - HARDWARE.md with hardware configuration guide
  - CONTRIBUTING.md with contribution guidelines
- Example scripts:
  - lvgl_basic.py - Basic LVGL display and touch example
  - ulab_demo.py - ulab numerical operations demonstration
  - lvgl_ulab_combined.py - Combined LVGL + ulab example
- Git submodule configuration for:
  - MicroPython (master branch)
  - LVGL v8 (release/v8.3 branch)
  - lv_binding_micropython (master branch)
  - ulab (master branch)
  - pycparser (master branch)
- CMake module configuration for integrating LVGL and ulab
- MIT License
- .gitignore for build artifacts and dependencies

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- N/A (initial release)

## Version History

### [0.1.0] - 2026-01-19

Initial release with basic project structure and build system for ESP32-S3.

---

## Guidelines for Updating

When adding entries:

- Group changes into categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Add most recent changes at the top of Unreleased section
- Link to relevant issues or pull requests
- Keep descriptions clear and concise
- Move unreleased changes to a new version section on release

Example entry:
```markdown
### Added
- Feature description [#123](link-to-issue)
- Another feature [#124](link-to-pr)

### Fixed
- Bug fix description [#125](link-to-issue)
```
