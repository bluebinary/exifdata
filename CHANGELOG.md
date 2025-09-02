# EXIFData Change Log

## [0.5.9] - 2025-09-01
### Added
- Added support for terminating ASCII strings with a NUL byte for EXIF metadata.

## [0.5.8] - 2025-09-01
### Added
- Added improved support for out-of-range characters in ASCII-only strings for EXIF metadata.

## [0.5.7] - 2025-08-20
### Added
- Added support for setting TIFF tag metadata on multiple IFDs within a single call.

## [0.5.6] - 2025-08-07
### Added
- Added support for the `SignedRational` data type in the EXIF metadata model.
- Added support for the `SignedByte` data type in the EXIF metadata model.
- Added support for the `SignedByte` data type in the EXIF metadata model.
- Added support for the `TIFFData` adapter.

### Changed
- Updated EXIF metadata model type class definitions.
- Updated dependency versions for `enumerific`, `deliciousbytes` and `maxml` libraries.

## [0.5.5] - 2025-06-12
### Added
- Reorganisation of several class files.
- Separation of large multi-class files into individual files for improved maintainability.
- Additional unit tests.

## [0.5.4] - 2025-06-11
### Added
- Metadata model documentation improvements.

## [0.5.3] - 2025-06-11
### Added
- Updated documentation, file cleanup, additional code comments.
- Adjusted the library to incorporate types from the `deliciousbytes` and `caselessly` libraries for improved long term maintenance.

## [0.5.2] - 2025-06-10
### Added
- Updated documentation, file cleanup, additional code comments.

## [0.5.1] - 2025-06-10
### Added
- Documentation improvements, and code example formatting fixes.

## [0.5.0] - 2025-06-10
### Added
- First (alpha) release of the EXIFData embedded metadata library.