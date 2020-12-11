import tensorflow as tf


def export_to_png(dataset: tf.data.Dataset, target_path: str):
    """ Export the given dataset to png images
    :param dataset: Dataset to export
    :param target_path: path where the images will be exported to.
    """
    from pathlib import Path
    from tqdm import tqdm
    for example in tqdm(dataset):
        filename = Path(target_path).joinpath(f'{example["id"]}V{example["visit"]}.png')
        encoded_image = tf.io.encode_png(example['image'])
        tf.io.write_file(filename, encoded_image)
