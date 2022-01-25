#!/usr/bin/env python

# BSD 3-Clause License
#
# Copyright (c) 2020, Stefan Reinhold
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
from os import PathLike
from typing import List, Dict, Union, IO, Tuple

import numpy as np


def load_table(file_path: Union[PathLike, str]) -> List[Dict]:
    """ Load key-point information table from .csv file
    :param file_path: Path to .csv file. If set to "-" will read from stdin.
    :return: key-point table as a list of dictionaries
    """
    from csv import DictReader

    def open_in() -> IO:
        """ Returns either the file stream or stdin
        """
        return sys.stdin if file_path == "-" else open(file_path)

    with open_in() as f:
        reader = DictReader(f)
        lines = [line for line in reader]
        return lines


def get_kp_vectors(table: List[Dict]) -> List[Dict]:
    """
    Coalesce all key-points from a row into one key-point vector.
    :param table: key-point table (as returned by
    load_table())
    :return: List of dictionary with keys: "id" (patient id), "lr" (hip side: [left, right]),
    "class" (classification class), "vector": key-point vector.
    """
    left_keys = [key for keys in [(f"left_kp{i}x", f"left_kp{i}y") for i in range(12)] for key in keys]
    right_keys = [key for keys in [(f"right_kp{i}x", f"right_kp{i}y") for i in range(12)] for key in keys]

    kp_vectors = [[
        {"id": row["id"], "lr": "left", "class": row["left_class"],
         "vector": np.array([float(row[key]) for key in left_keys])},
        {"id": row["id"], "lr": "right", "class": row["right_class"],
         "vector": np.array([float(row[key]) for key in right_keys])}
    ] for row in table]

    # Filter out any non "complete" classes, since they do not contain meaningfull key-points
    kp_vectors = [entry for entries in kp_vectors for entry in entries if entry["class"].lower() == "complete"]

    return kp_vectors


def compute_descriptor(row: Dict) -> Dict:
    """
    Computes a descriptor vector given a row containing a key-point vector.
    :param row: dictionary that must contain at least a key-point vector ("vector" key) and a side entry ("lr" key).
    :return: `row` with an added "descriptor" entry
    """
    vector = row["vector"]
    positions = vector.reshape((-1, 2))

    # Flip right positions to "simulate" left ones
    if row["lr"] == "right":
        positions[:, 0] = 1 - positions[:, 0]

    distance_matrix = np.sqrt(np.square(positions[:, 0, np.newaxis] - positions[np.newaxis, :, 0]) + np.square(
        positions[:, 1, np.newaxis] - positions[np.newaxis, :, 1]))
    N = positions.shape[0]
    distance_vect = []
    for i in range(N - 1):
        for j in range(i + 1, N):
            distance_vect += [np.abs(distance_matrix[i, j])]

    row["descriptor"] = np.concatenate([vector, distance_vect], axis=0)
    return row


def compute_statistics(rows: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute the statistics (mean and covariance matrix) for the given rows
    :param rows: list of dictionaries that have a descriptor vector with the key "descriptor"
    :return: mean and covariance matrix as numpy arrays
    """
    assert len(rows) > 1
    data_matrix = np.array([row["descriptor"] for row in rows])
    mean = np.mean(data_matrix, axis=0)
    cov_matrix = np.matmul((data_matrix - mean).transpose(), data_matrix - mean) / (data_matrix.shape[0] - 1)
    return mean, cov_matrix


def find_outliers(table, confidence=0.95):
    """
    Search for outliers in the given key-point table. All data points that are outside the confidence interval are
    considered as outliers.
    :param table: key-point table as returned by `load_table()`
    :param confidence: confidence
    interval use for the outlier search. Defaults to 0.95.
    :return: all entries of `table` that are classified as
    outliers. Note that one row may produce two entries, since the left and the right hips are treated separately.
    """
    from scipy.stats import chi2

    # Compute descriptors
    rows = get_kp_vectors(table)
    descriptors = [compute_descriptor(row) for row in rows]
    # Compute statistics
    mean, cov = compute_statistics(descriptors)

    # data is the NxM data matrix, where M is the number of dimensions of the descriptor.
    data = np.array([row["descriptor"] for row in rows])
    # Use cholesky decomposition to compute cov^0.5
    chol = np.linalg.cholesky(cov)
    # Multiply the (centered) data points with the cov^(-0.5) by solving a system of linear equations
    distance_sq = np.sum(np.square(np.linalg.solve(chol, (data - mean).transpose())), axis=0)
    # Compute the radius of the confidence sphere
    radius_sq = chi2.ppf(confidence, data.shape[1])

    return [x for (x, d) in zip(rows, distance_sq) if d > radius_sq]


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Detect outliers in the detected key-points. Prints out the patient id and the side of any '
                    'outliers, therefore, e.g. the key points of the right hip might be detected as outliers while '
                    'the key points of the left hip of the same patient might not.')
    parser.add_argument('csv_file', type=str, help='Path to .csv file containing the key point information')
    parser.add_argument('-V', '--version', action='store_true',
                        help="Print the version string")
    parser.add_argument('-i', '--interval', type=float, default=0.95,
                        help='Confidence interval all inliers should lie in, default to 095.')
    parser.add_argument('-f', '--file', type=str, default='-', help='Write output to file instead of stdout')

    args = parser.parse_args()

    if args.version:
        import sof_utils
        print(sof_utils.__version__)
        exit(0)

    table = load_table(args.csv_file)
    outliers = find_outliers(table, args.interval)

    def open_out() -> IO:
        """ Returns a stream to the output file (stdout in case of "-")
        """
        return sys.stdout if args.file == "-" else open(args.file)

    with open_out() as f:
        f.write("id,side\n")
        lines = [f"{row['id']},{row['lr']}\n" for row in outliers]
        f.writelines(lines)


if __name__ == '__main__':
    main()
