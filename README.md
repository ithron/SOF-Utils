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
                         [--width WIDTH] [--height HEIGHT] [--split_lr]
                         [--flip_lr] [--visits VISITS] [--include INCLUDE]
                         [--exclude EXCLUDE] [--max-group-size MAX_GROUP_SIZE]
                         [--num-groups NUM_GROUPS] [--randomized-groups]
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
  --width WIDTH, -w WIDTH
                        Target width of the exported images
  --height HEIGHT, -g HEIGHT
                        Target height of the exported images
  --split_lr, -s        Split radiographs vertically into a left and a right
                        half. The exported files will get a "L" or "R"
                        postfix, depending on the side of the hip that is
                        shown. Note that the left hip is usually shown on the
                        right hand side of the radiograph. If the (possibly
                        downscaled) image does not have an even width, it is
                        padded with one additional volumn to the right.
  --flip_lr, -p         Flips the images of the left hip so that they look
                        like a right hip. Can only be used in combination with
                        --flip_lr
  --visits VISITS, -v VISITS
                        Comma separated list of visits to export. If this
                        option is omitted, all visits are exported.
  --include INCLUDE     Only include the IDs listed in given file. The IDs
                        should be listed one ID per line.
  --exclude EXCLUDE     Exclude the IDs listed in given file. The IDs should
                        be listed one ID per line.
  --max-group-size MAX_GROUP_SIZE
                        Splits the exported images into groups. The groups
                        will contain at most the specific number of files.
                        Cannot be used together width --num-groups
  --num-groups NUM_GROUPS
                        Splits the exported images into the specified number
                        of groups. Cannot be used together with --max-group-
                        size.
  --randomized-groups   If grouping is used (either with --max-group-size or
                        with --num-groups), the assignment of files to groups
                        will be randomized.
```

### sof-convert-labels
```text
usage: sof-convert-labels [-h] [-V] [-f FILE] input_label_file

Convert proximal femur bounding box annotations from label-studio to csv
format

positional arguments:
  input_label_file      Path to input label json file.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print the version string
  -f FILE, --file FILE  Write output to file instead to stdout
```
