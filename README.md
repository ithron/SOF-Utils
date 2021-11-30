# SOF-Utils

[![PyPI version](https://badge.fury.io/py/sof-utils.svg)](https://badge.fury.io/py/sof-utils)

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
                         [--zip]
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
  --zip, -z             Write exported images to a zip file instead of into a
                        directory. If grouping is enabled, one zip file per
                        group will be created. Without grouping 'target_path'
                        should be a path a the target zip file not to an
                        directoty.
```

### sof-convert-labels
```text
usage: sof-convert-labels [-h] [-V] [-f FILE] [-s SKIP_FILE] input_label_file

Convert proximal femur labels from LabelStudio JSON_MIN format to csv format

positional arguments:
  input_label_file      Path to input label json file(s). Multiple files can
                        be used using glob pattern.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print the version string
  -f FILE, --file FILE  Write output to file instead to stdout
  -s SKIP_FILE, --skip-file SKIP_FILE
                        Write skipped file names to the given file.
```

### sof-convert-tfds
```text
usage: sof-convert-tfds [-h] [--data_dir DATA_DIR] [-V]
                        [--configuration {keypoint_detection}]
                        [--format {TFObjectDetection}] [--split SPLIT]
                        [--num_shards NUM_SHARDS]
                        output_file

Convert SOF_hip TFDS dataset into another format.

positional arguments:
  output_file           Path to destination file.

optional arguments:
  -h, --help            show this help message and exit
  --data_dir DATA_DIR   TFDS data dir.
  -V, --version         Print the version string
  --configuration {keypoint_detection}, -c {keypoint_detection}
                        Dataset configuration to use. Note: not all
                        configuration are supported by all output format.
                        Default is 'keypoint_detection'
  --format {TFObjectDetection}, -f {TFObjectDetection}
                        Dataset configuration to use. Note: not all
                        configuration are supported by all output format.
                        Default is 'TFObjectDetection'
  --split SPLIT, -s SPLIT
                        Split to convert. Default to 'train'
  --num_shards NUM_SHARDS, -n NUM_SHARDS
                        Number of shards to split the resulting dataset into.
```

### sof-detect-keypoints
```text
usage: sof-detect-keypoints [-h] [-f FILE] [-V] [--data_dir DATA_DIR]
                            [--configuration {unsupervised_raw,unsupervised_raw_tiny}]
                            [--preview-dir PREVIEW_DIR]
                            model_path

Detect keypoints on hip radiographs. Important: the TFDS SOF_hip package must
be in the python path.

positional arguments:
  model_path            Path to saved detection model.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Write CSV data to the given file instead of stdout.
  -V, --version         Print the version string
  --data_dir DATA_DIR, -d DATA_DIR
                        Path to the TFDS dataset.
  --configuration {unsupervised_raw,unsupervised_raw_tiny}, -c {unsupervised_raw,unsupervised_raw_tiny}
                        Dataset configuration.
  --preview-dir PREVIEW_DIR, -p PREVIEW_DIR
                        If given, path to write images with visualizations of
                        keypoints to.
  --from-images FROM_IMAGES, -i FROM_IMAGES
                        Detect keypoint from png images instead of the SOF_hip TFDS dataset
```

#### Table Description
The table generated by `sof-detect-keypoints` has the following columns:
<dl>
	<dt>id</dt>
	<dd>The patient's SOF ID</dd>
	<dt>visit</dt>
	<dd>The visit where the radiograph was taken</dd>
	<dt>width</dt>
	<dd>Width in pixel of the (padded) radiograph.</dd>
	<dt>height</dt>
	<dd>Height in pixel of the (padded) radiograph.</dd>
	<dt>upside_down</dt>
	<dd>Orientation of the radiograph. A <strong>1</strong> indicates that the radiograph must be flipped vertically <strong>and</strong> horizontally. A <strong>0</strong> means no flipping is required.</dd>
	<dt>left_class</dt>
	<dd>Class of the <strong>left femur</strong>. One of 'Complete', 'Incomplete' or 'Implant'</dd>
	<dt>left_score</dt>
	<dd>Detection score for the <strong>left femur</strong> in the range [0, 1].</dd>
	<dt>right_class</dt>
	<dd>Class of the <strong>right femur</strong>. One of 'Complete', 'Incomplete' or 'Implant'</dd>
	<dt>right_score</dt>
	<dd>Detection score for the <strong>right femur</strong> in the range [0, 1].</dd>
	<dt>left_kp{i}x</dt>
	<dd>For <strong>i</strong> in {0, ..., 11}.Normalized x-coordinate of the <strong>i</strong>-th key point of the <strong>left femur</strong>. In the range [0, 1].</dd>
	<dt>left_kp{i}y</dt>
	<dd>For <strong>i</strong> in {0, ..., 11}.Normalized y-coordinate of the <strong>i</strong>-th key point of the <strong>left femur</strong>. In the range [0, 1].</dd>
	<dt>right_kp{i}x</dt>
	<dd>For <strong>i</strong> in {0, ..., 11}.Normalized x-coordinate of the <strong>i</strong>-th key point of the <strong>right femur</strong>. In the range [0, 1].</dd>
	<dt>right_kp{i}y</dt>
	<dd>For <strong>i</strong> in {0, ..., 11}.Normalized y-coordinate of the <strong>i</strong>-th key point of the <strong>right femur</strong>. In the range [0, 1].</dd>
</dl>

**Note**: for classes other than `Complete` all key points are `(0, 0)`.
Also note that the **left_\{...\}** and **right_\{...\}** always correspond to the left and right femur, not the left hand or right hand side of the image. The left femur is usually located on the right hand side of the radiograph.
