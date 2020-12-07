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