# Changelog

## Upcoming release
# Fixed
- Added missing requirement 'contextlib2'

## v0.2.0
### Added
- One can now specify the data set split in `sof-export-images`.

## v0.1.3
### Fixed
- fixed compatibility of `sof-export-images` with SOF_hip v1.0.6

## v0.1.2
### Improved
- `sof-convert-labels` now accepts a wider range of filename patterns

## v0.1.1
### Fixed
- Missing requirement: scipy

## v0.1.0
### Added

- `sof-keypoint-outlier` tool to detect outlier in the result of `sof-detect-keypoints`.

## v0.0.23
### Fixed
- The package `SOF_hip` is no longer required when using png files instead of the TFDS data set.
- The `sof-detect-keypoints` section in the README.md was outdated.

## v0.0.22
### Fixed
- A typo in _requirements.txt_ resulted in failed installation

## v0.0.21
### Fixed
- `sof-detect-keypoints` missing in install script
- missing _tensorflow-dataset_ requirement
### Added
- `sof-detect-keypoints` now also works with png images (not only TFDS datasets)

## v0.0.20
### Fixed
- [Issue 14](https://github.com/ithron/OF-Utils/issues/14): sof-detect-keypoints: wrong upside_down label on rare case with wrong key point locations and low confidence

## v0.0.19
### Fixed
- `sof-detect-keypoints` processes only 10 images.

## v0.0.18
### Fixed
- `sof-detect-keypoints` crashes when writing CSV file

## v0.0.16
### Added
  - `sof-detect-keypoints` tool to detect keypoints on the `SOF_hip` dataset.

## v0.0.15

### Added

- `sof-convert-tfds` now included `image/upside_down` labels

## 0.0.14

### Fixed

- Fixed: `sof-convert-tfds` ignores class labels.

## 0.0.13

### Added
- `sof-convert-labels` can now handle multiple input files

## 0.0.12

### Fixed

- pypi package badge

## 0.0.11

### Added

- pypi package badge

## 0.0.10

### Added

- `sof-convert-tfds` tool to convert the TFDS dataset to other formats.

### Changed

- Adapted `sof-convert-labels` tool to new LabelStudio label format (including key points).

## 0.0.9
### Added

- `sof-convert-labels` tool to convert proximal femur detection labels from label-studio json format to a short csv format.
- Options for `sof-export-images` tool to split images into left and right half.
- Option for `sof-export-images` to only export selected visits.
- Option for `sof-export-images` to include or exclude SOF IDs listed in files.
- Options to group the exported images (`--num-groups`, `--max-group-size` and `--randomized-groups`).
- Option `--zip` for `sof-export-images` to write expoted image directly to (a) zip archive(s).

### Removed

- Deprecated and dysfunctional `--jpeg` option for the `sof-export-images` tool

## 0.0.7
### Added

- Image export tool

## 0.0.6
### Added

- Tool to export the images from the SOF_hip dataset to PNG or JPG files.
- Function to extract ID and visit from a filename 

## 0.0.5

### Added

- Package version can be now accessed at runtime using `sof_utils.__version__`
- CLI script now have an option to show the version `-V`
- Function to load pixel data from DICOM files.

## 0.0.4

Released on December 7, 2020

### Fixed

- `sof-dicom-corrupted` does not show percentage or ETA when run with `-p`

## 0.0.3

Released on December 7, 2020

### Added

- `sof-dicom-corrupted` command line tool to find corrupted DICOM files  

### Changed

- The progressbar of the CLI tools now shows an ETA and a percentage

## 0.0.2

Released on December 4, 2020

### Added

- `sof-dicom-meta` CLI tool to extract image dimensions and main/max pixel values from DICOM files 
