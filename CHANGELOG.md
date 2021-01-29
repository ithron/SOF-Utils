# Changelog

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