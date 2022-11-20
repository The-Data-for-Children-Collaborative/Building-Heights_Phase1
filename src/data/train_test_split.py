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


def add_vhms_to_csvs(folder):

    splits = ["train", "test"]

    for split in splits:

        with open(folder + "pairings_" + split + ".csv", "r") as f:
            filenames = f.readlines()

        with open(folder + "triplets_" + split + ".csv", "w") as f:
            for filename in filenames:
                maxar, bhm = filename.split(",")
                vhm = bhm.replace("bhm", "vhm")
                newline = ",".join([maxar, bhm.strip(), vhm])
                f.write(newline)


def make_train_test_dirs(folder, train_csv, test_csv, zip=False):

    # make directories if they don't exist
    dir_bhm_train = folder + "train_bhm_sliced/"
    dir_bhm_test = folder + "test_bhm_sliced/"
    dir_vhm_train = folder + "train_vhm_sliced/"
    dir_vhm_test = folder + "test_vhm_sliced/"
    dir_maxar_train = folder + "train_maxar_sliced/"
    dir_maxar_test = folder + "test_maxar_sliced/"

    for dir in [
        dir_bhm_train,
        dir_bhm_test,
        dir_vhm_train,
        dir_vhm_test,
        dir_maxar_train,
        dir_maxar_test,
    ]:
        try:
            os.mkdir(dir)
        except FileExistsError:
            pass

    copy_files(folder, train_csv, dir_maxar_train, dir_bhm_train, dir_vhm_train)
    copy_files(folder, test_csv, dir_maxar_test, dir_bhm_test, dir_vhm_test)


def copy_files(
    input_dir, input_filename, maxar_output_dir, bhm_output_dir, vhm_output_dir
):

    with open(input_dir + input_filename) as f:
        lines = f.readlines()

    for i, filenames in enumerate(lines):
        maxar_filename, bhm_filename, vhm_filename = filenames[:-1].split(",")
        print(i, "/", len(lines))
        maxar_array = np.load(input_dir + "sliced_maxar/" + maxar_filename)
        bhm_array = np.load(input_dir + "sliced_bhm/" + bhm_filename)
        try:
            vhm_array = np.load(input_dir + "sliced_vhm/" + vhm_filename)
        except FileNotFoundError:
            print("vhm file", vhm_filename, "not found: making array of zeros")
            vhm_array = np.zeros_like(bhm_array)
        if (
            np.shape(maxar_array) == (500, 500, 4)
            and np.shape(bhm_array) == (500, 500)
            and np.shape(vhm_array) == (500, 500)
        ):
            np.save(maxar_output_dir + maxar_filename, maxar_array)
            np.save(bhm_output_dir + bhm_filename, bhm_array)
            np.save(vhm_output_dir + vhm_filename, vhm_array)
        else:
            print("Error in dimensions: check slicing for file", maxar_filename)


if __name__ == "__main__":

    folder = "/home/tim/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_10/"

    force_overwrite = True
    if not os.path.isfile(folder + "pairings_train.csv") or force_overwrite:
        print("making csvs")
        make_split_csvs(folder, "pairings.csv")
        add_vhms_to_csvs(folder)
    make_train_test_dirs(folder, "triplets_train.csv", "triplets_test.csv")
