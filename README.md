# SOF-Utils

Utility scripts to aid working with the SOF dataset.

## Command Line Tools

### sof-dicom-meta
```text
usage: sof-dicom-meta [-h] [-r] [-f FILE] [-p] [-s] dicom_path

Extract dicom meta info in csv format.

positional arguments:
  dicom_path            Path to search for dicom files in.

optional arguments:
  -h, --help            show this help message and exit
  -r                    Inlcude subdirectories
  -f FILE, --file FILE  Write output to file instead of stdout.
  -p, --progress        Shows a progressbar, only available in combination
                        with -f.
  -s, --statistics      Print minimum and maximum values for each column.
```

### sof-dicom-corrupted
```text
usage: sof-dicom-corrupted [-h] [-r] [-f FILE] [-p] [-d] [-s] dicom_path

Find corrupted dicom files.

positional arguments:
  dicom_path            Path to search for dicom files in.

optional arguments:
  -h, --help            show this help message and exit
  -r                    Inlcude subdirectories
  -f FILE, --file FILE  Write output to file instead of stdout.
  -p, --progress        Shows a progressbar, only available in combination
                        with -f.
  -s, --summary         Print summary.
```

### sof-export-images
```text
usage: sof-export-images [-h] [-V] [--data_dir DATA_DIR]
                         [--configuration CONFIGURATION] [--format {png,jpeg}]
                         [--jpeg] [--width WIDTH] [--height HEIGHT]
                         target_path

Exports the SOF_hip dataset as png images

positional arguments:
  target_path           Path to place the images in.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print the version string
  --data_dir DATA_DIR, -d DATA_DIR
                        Path to the TFDS dataset.
  --configuration CONFIGURATION, -c CONFIGURATION
                        Dataset configuration.
  --format {png,jpeg}, -t {png,jpeg}
                        Output image format, default to png
  --jpeg                Export JPEGs instead of PNGs.
  --width WIDTH, -w WIDTH
                        Target width of the exported images
  --height HEIGHT, -g HEIGHT
                        Target height of the exported images
```
