#!/usr/bin/env python

import sys
import tensorflow_datasets as tfds
import SOF_hip
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
import numpy as np

_CLASS_LABELS = [
    "complete",
    "incomplete",
    "implant"
]

def plot_example(example):
    img = tf.cast(tf.repeat(example['image'][tf.newaxis, ...], 3, axis=-1), dtype=tf.float32) / 255

    bbox = example['object/bbox'][tf.newaxis, tf.newaxis, ...]
    color = np.array([[1.0, 0.0, 0.0]])
    color2 = np.array([[0.0, 1.0, 0.0]])

    class_id = example['object/class'].numpy()
    class_label = _CLASS_LABELS[class_id]

    annotated_img = tf.image.draw_bounding_boxes(img, bbox, color)

    x_offset = 1/float(img.shape[-2])
    y_offset = 1/float(img.shape[-3])
    offset = tf.convert_to_tensor(np.array([-y_offset, -x_offset, y_offset, x_offset]), dtype=tf.float32)[tf.newaxis, tf.newaxis]

    kp_bb = example['object/keypoints'][tf.newaxis, ...]
    kp_bb = tf.concat([kp_bb, kp_bb], axis=-1) + offset

    annotated_img = tf.image.draw_bounding_boxes(annotated_img, kp_bb, color2)

    plt.imshow(annotated_img.numpy().squeeze())
    plt.title(f"{example['image/id'].numpy()}V{example['image/visit'].numpy()}{example['image/left_right'].numpy().decode('utf8')} - {class_label} [{class_id}]")
    plt.show()

if __name__ == '__main__':
    # from object_detection.data_decoders.tf_example_decoder import TfExampleDecoder
    # data = tf.data.TFRecordDataset(sys.argv[1])
    # decoder = TfExampleDecoder()
    # for encoded_example in data:
    #     example = decoder.decode(encoded_example)
    #     plot_example(example)
    ds = tfds.load('SOF_hip/keypoint_detection', split='train', data_dir='/data-dest/tfds')

    for i, example in enumerate(ds):
        plot_example(example)
        # if i > 9:
        #     break



