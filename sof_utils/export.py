from typing import Tuple, Union, List

import tensorflow as tf


def export_images(dataset: tf.data.Dataset,
                  target_path: str,
                  format: str = 'png',
                  downsample_to: Tuple[Union[int, None], Union[int, None]] = (1, None),
                  split_lr: bool = False,
                  flip_lr: bool = False,
                  visits: List[int] = []):
    """ Export the given dataset to png images
    :param dataset: Dataset to export
    :param target_path: path where the images will be exported to.
    :param format: image format to use: png (default) or jpeg
    :param downsample_to: target (width, height) of exported image (defaults to (None, None)).
        If one entry is None, it is inferred from the other one by keeping the aspect ratio.
        If booth entries are None, the original size is kept.
    :split_lr: if true (default is false), splits the image vertically into a left and a right part, i.e. two instead of
        one image files are written per example.
    :flip_lr: if true (default is false), flips the right part of the image vertically. Does nothing if
        'split_lr == False'.
    """
    from pathlib import Path
    from tqdm import tqdm
    from math import ceil

    target_path = Path(target_path)
    target_path.mkdir(parents=True, exist_ok=True)

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
        if visits and example['visit'] not in visits:
            continue

        image = tf.cast(tf.image.resize(example['image'], (downsample_to[1], downsample_to[0])), dtype=tf.uint8)

        if split_lr:
            left_img, right_img = split_image_lr(image, flip_lr)
            postfix = f"-{left_img.shape[1]}x{left_img.shape[0]}"
            # write left image, ie.e right hip
            filename = target_path.joinpath(f'{example["id"]}V{example["visit"]}R{postfix}.png')
            encoded_image = encoding_func(left_img)
            tf.io.write_file(str(filename), encoded_image)

            # write right image, i.e. left hip
            filename = target_path.joinpath(f'{example["id"]}V{example["visit"]}L{postfix}.png')
            encoded_image = encoding_func(left_img)
            tf.io.write_file(str(filename), encoded_image)
        else:
            postfix = f"-{image.shape[1]}x{image.shape[0]}"
            filename = target_path.joinpath(f'{example["id"]}V{example["visit"]}{postfix}.png')
            encoded_image = encoding_func(image)
            tf.io.write_file(str(filename), encoded_image)


def split_image_lr(image: tf.Tensor, flip_lr: bool = False) -> Tuple[tf.Tensor, tf.Tensor]:
    """ Split image vertically into a left and a right image.
    If the image does not have an even width, it is padded by one column at the right.
    :param image: source image to split
    :param flip_lr: If true, flips the right image vertically.
    :return: (left_image, right_image) tuple containing the left and the right half of the image.
    """
    padding = image.shape[1] % 2
    padded_image = tf.image.pad_to_bounding_box(image, 0, 0, image.shape[0], image.shape[1] + padding)

    image_half_width = tf.cast(tf.math.ceil(padded_image.shape[1] / 2), tf.int64)

    left_image = padded_image[..., 0:image_half_width, :]
    right_image = padded_image[..., image_half_width:, :]

    if flip_lr:
        right_image = tf.image.flip_left_right(right_image)

    return left_image, right_image
