import random
import os
import shutil
import numpy as np


def make_split_csvs(folder, filename, train_frac=0.85):
    with open(folder + "pairings.csv", "r") as f:
        lines = f.readlines()
    header = lines[0]
    lines = lines[1:]

    random.shuffle(lines)

    N_tot = len(lines)
    N_train = int(train_frac * N_tot)

    train_files = lines[:N_train]
    test_files = lines[N_train:]

    with open(folder + "pairings_train.csv", "w") as f:
        for filename in train_files:
            f.write(filename)

    with open(folder + "pairings_test.csv", "w") as f:
        for filename in test_files:
            f.write(filename)


def make_train_test_dirs(folder, train_csv, test_csv, zip=False):

    # make directories if they don't exist
    dir_bhm_train = folder + "train_bhm_sliced/"
    dir_bhm_test = folder + "test_bhm_sliced/"
    dir_maxar_train = folder + "train_maxar_sliced/"
    dir_maxar_test = folder + "test_maxar_sliced/"

    try:
        os.mkdir(dir_bhm_test)
        os.mkdir(dir_bhm_train)
        os.mkdir(dir_maxar_test)
        os.mkdir(dir_maxar_train)
    except FileExistsError:
        pass

    copy_files(folder, train_csv, dir_maxar_train, dir_bhm_train)
    copy_files(folder, test_csv, dir_maxar_test, dir_bhm_test)


def copy_files(input_dir, input_filename, maxar_output_dir, bhm_output_dir):

    with open(input_dir + input_filename) as f:
        lines = f.readlines()

    for i, filenames in enumerate(lines):
        maxar_filename, bhm_filename = filenames[:-1].split(",")
        print(i, "/", len(lines))
        maxar_array = np.load(input_dir + "sliced_maxar/" + maxar_filename)
        bhm_array = np.load(input_dir + "sliced_bhm/" + bhm_filename)
        if np.shape(maxar_array) == (500, 500, 4):
            shutil.copyfile(
                input_dir + "sliced_maxar/" + maxar_filename,
                maxar_output_dir + maxar_filename,
            )
        if np.shape(bhm_array) == (500, 500):
            shutil.copyfile(
                input_dir + "sliced_bhm/" + bhm_filename, bhm_output_dir + bhm_filename
            )


if __name__ == "__main__":

    folder = "/home/tim/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_16/"

    if not os.path.isfile(folder + "pairings_train.csv"):
        make_split_csvs(folder, "pairings.csv")

    make_train_test_dirs(folder, "pairings_train.csv", "pairings_test.csv")
