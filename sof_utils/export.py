from typing import Tuple, Union

import tensorflow as tf


def export_images(dataset: tf.data.Dataset,
                  target_path: str,
                  format: str = 'png',
                  downsample_to: Tuple[Union[int, None], Union[int, None]] = (1, None)):
    """ Export the given dataset to png images
    :param dataset: Dataset to export
    :param target_path: path where the images will be exported to.
    :param format: image format to use: png (default) or jpeg
    :param downsample_to: target (width, height) of exported image (defaults to (None, None)).
        If one entry is None, it is inferred from the other one by keeping the aspect ratio.
        If booth entries are None, the original size is kept.
    """
    from pathlib import Path
    from tqdm import tqdm
    from math import ceil

    if format.lower() == 'png':
        encoding_func = lambda x: tf.io.encode_png(x)
    elif format.lower() == 'jpeg':
        encoding_func = lambda x: tf.io.encode_jpeg(x)
    else:
        raise ValueError(f"Unsupported image format: {format}. supported formats are: png, jpeg")

    image_shape = next(iter(dataset))['image'].shape

    # Compute missing downsample_to entry, if any
    if not downsample_to[0] and not downsample_to[1]:
        downsample_to = (image_shape[1], image_shape[0])
    elif not downsample_to[0]:
        ratio = float(downsample_to[1]) / float(image_shape[0])
        downsample_to = (int(ceil(ratio * float(image_shape[0]))), downsample_to[1])
    elif not downsample_to[1]:
        ratio = float(downsample_to[0]) / float(image_shape[1])
        downsample_to = (downsample_to[0], int(ceil(ratio * float(image_shape[1]))))

    for example in tqdm(dataset):
        filename = Path(target_path).joinpath(f'{example["id"]}V{example["visit"]}.png')
        image = tf.cast(tf.image.resize(example['image'], downsample_to), dtype=tf.uint8)
        encoded_image = encoding_func(image)
        tf.io.write_file(str(filename), encoded_image)
