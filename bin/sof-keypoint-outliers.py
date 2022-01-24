#!/usr/bin/env python
import sys

import numpy as np


def load_table(file_path):
    from csv import DictReader

    with open(file_path) as f:
        reader = DictReader(f)
        lines = [line for line in reader]
        return lines


def get_kp_vectors(table):
    left_keys = [key for keys in [(f"left_kp{i}x", f"left_kp{i}y") for i in range(12)] for key in keys]
    right_keys = [key for keys in [(f"right_kp{i}x", f"right_kp{i}y") for i in range(12)] for key in keys]

    kp_vectors = [[
        {"id": row["id"], "lr": "left", "class": row["left_class"],
         "vector": np.array([float(row[key]) for key in left_keys])},
        {"id": row["id"], "lr": "right", "class": row["right_class"],
         "vector": np.array([float(row[key]) for key in right_keys])}
    ] for row in table]

    kp_vectors = [entry for entries in kp_vectors for entry in entries if entry["class"].lower() == "complete"]

    return kp_vectors


def compute_descriptor(row):
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


def compute_statistics(rows):
    assert len(rows) > 1
    data_matrix = np.array([row["descriptor"] for row in rows])
    mean = np.mean(data_matrix, axis=0)
    cov_matrix = np.matmul((data_matrix - mean).transpose(), data_matrix - mean) / (data_matrix.shape[0] - 1)
    return mean, cov_matrix


def find_outliers(table, confidence=0.95):
    from scipy.stats import chi2

    rows = get_kp_vectors(table)
    descriptors = [compute_descriptor(row) for row in rows]
    mean, cov = compute_statistics(descriptors)

    data = np.array([row["descriptor"] for row in rows])
    chol = np.linalg.cholesky(cov)
    distance_sq = np.sum(np.square(np.linalg.solve(chol, (data - mean).transpose())), axis=0)
    radius_sq = chi2.ppf(confidence, data.shape[1])

    return [x for (x, d) in zip(rows, distance_sq) if d > radius_sq]


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Detect outliers in the detected key-points')
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
    f_fun = lambda f: sys.stdout if f == '-' else open(f)
    with f_fun(args.file) as f:
        f.write("id,side\n")
        lines = [f"{row['id']},{row['lr']}\n" for row in outliers]
        f.writelines(lines)

if __name__ == '__main__':
    main()
