"""
This script has two main functions:

1. It filters out BHM and maxar images based on one of two criteria, either:
   (i) The number of pixels in the x and y directions (removes small images), or
   (ii) The difference between the measured pixel resolution in m and the actual
        pixel resolution
(i) and (ii) are strongly correlated, but (i) should be preferred because it is
more consistent in filtering out the same images from each dataset.

2. It copies the files that passed the filter to a new location, and gives them
more consistent names in the process. It breaks the images into smaller sub-folders
and zips them up for easier transfer.

Information about the files to filter and copy are contained in two csv files. These
files are created by the height_model_file_edges.py module, which is called during
the data pipeline process (regrid_maxar.py). Please see the
data/processed/BHM_maxar_csv_files folder of this repository for examples of these
files.

It is expected that this script is run from somewhere with direct access to the S3
data bucket. It will require some modifications to run from a different location.
"""

import pandas as pd
import numpy as np
import os
from os.path import expanduser
import shutil

###     USER INPUTS     ###

# tolerance for error in pixel resolution in m: if the average pixel length
# differs by more than err_tol from the expected value, it is filtered out
err_tol = 0.01
pixel_base = 0.5  # expected pixel size in m
pixel_small = 100  # minimum pixel size in x & y directions
chunk_size = 100  # size to break full dataset into
# filter on resolution (pixel_resolution) or dimensions (pixel_dimensions)
filter_criterion = "pixel_dimensions"  # dimensions always recommended

### END OF USER INPUTS ###

# get the home directory
homedir = expanduser("~")

# get the data path
basedir = homedir + "/data/UNICEF_data"

# csv files
csv_bhm = basedir + "/summary_data/BHM_pm.csv"
csv_maxar = basedir + "/summary_data/maxar_pm.csv"

# make a directory for the new file pairs
datapath = basedir + "/tim_maxar_bhm_final_pairs"

# read in the dataframes
df_bhm = pd.read_csv(csv_bhm)
df_maxar = pd.read_csv(csv_maxar)

# get a filecode column which can be used to match the two dfs
df_bhm["file_code"] = df_bhm.file_name.str[:8].str.split("-").str.join("").astype(int)
df_maxar["file_code"] = (
    df_maxar.file_name.str[:8].str.split("_").str.join("").astype(int)
)

# create pixel error x,y columns (difference between expected and actual pixel size)
dfs = [df_bhm, df_maxar]
for df in dfs:
    df["pixel_err_x"] = np.abs(((df.right - df.left) / df.pixel_horiz) - 0.5)
    df["pixel_err_y"] = np.abs(((df.top - df.bottom) / df.pixel_vert) - 0.5)

# filter images with small pixel numbers
if filter_criterion == "pixel_dimensions":
    df_bhm = df_bhm.loc[
        (df_bhm["pixel_horiz"] > pixel_small) & (df_bhm["pixel_vert"] > pixel_small)
    ]
    df_maxar = df_maxar.loc[
        (df_maxar["pixel_horiz"] > pixel_small) & (df_maxar["pixel_vert"] > pixel_small)
    ]
# or filter images with errors in the pixel size
else:
    df_bhm = df_bhm.loc[
        (df_bhm["pixel_err_x"] <= err_tol) & (df_bhm["pixel_err_y"] <= err_tol)
    ]
    df_maxar = df_maxar.loc[
        (df_maxar["pixel_err_x"] <= err_tol) & (df_maxar["pixel_err_y"] <= err_tol)
    ]

# reduce the maxar dataset so it fully interesects with the bhm set
df_maxar = df_maxar.loc[df_maxar["file_code"].isin(df_bhm["file_code"].values)]

# sort by file code and drop indices so the rows in both files line up
df_bhm = df_bhm.sort_values("file_code", ascending=True)
df_maxar = df_maxar.sort_values("file_code", ascending=True)
df_maxar = df_maxar.reset_index(drop=True)
df_bhm = df_bhm.reset_index(drop=True)

# add hyphen back into file codes
df_bhm.file_code = (
    df_bhm.file_code.astype("str").str[:4]
    + "-"
    + df_bhm.file_code.astype("str").str[4:]
)
df_maxar.file_code = (
    df_maxar.file_code.astype("str").str[:4]
    + "-"
    + df_maxar.file_code.astype("str").str[4:]
)

# copy files in loop
# split this into chunks
num_chunks = len(df_maxar) // chunk_size + 1

chunk_sizes = chunk_size + np.zeros((num_chunks), dtype=int)
chunk_sizes[-1] = num_chunks * chunk_size - len(df_maxar)

for j in range(num_chunks):
    subpath = datapath + "/pairs" + "_" + str(j)
    try:
        os.makedirs(subpath)
        os.makedirs(subpath + "/maxar")
        os.makedirs(subpath + "/bhm")
    except FileExistsError:
        pass

    print("Zipping chunk", j + 1, " / ", num_chunks)
    for k in range(chunk_sizes[j]):
        i = k + j * chunk_sizes[j]

        # make new filenames cleaner
        new_maxar_name = subpath + "/maxar/maxar-" + str(df_maxar.file_code[i]) + ".tif"
        old_maxar_name = (
            basedir
            + "/kaggle_maxar_tiles_copy/data/maxar_tiles/"
            + df_maxar.file_name[i]
        )

        new_bhm_name = subpath + "/bhm/bhm-" + str(df_bhm.file_code[i]) + ".tif"
        old_bhm_name = (
            basedir
            + "/height-model-copy/"
            + df_bhm.file_code[i][:4]
            + "-BHM/BHM-"
            + df_bhm.file_name[i]
            + ".tif"
        )

        shutil.copyfile(old_maxar_name, new_maxar_name)
        shutil.copyfile(old_bhm_name, new_bhm_name)

    # zip the files
    shutil.make_archive(datapath + "/maxar_bhm_pairs_" + str(j), "zip", subpath)
