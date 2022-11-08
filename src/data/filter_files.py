import pandas as pd
import numpy as np
import os
import shutil

# error tolerance
err_tol = 0.01
pixel_base = 0.5
pixel_small = 100
filter_criterion = "pixel_size"

csv_bhm = "/home/tim/data/UNICEF_data/summary_data/BHM_subset_pm_res.csv"
csv_maxar = "/home/tim/data/UNICEF_data/summary_data/maxar_subset_pm.csv"
# csv_bhm = "/home/tim/Autumn22_DFCCU/data/processed/BHM_subset_pm_res.csv"
# csv_maxar = "/home/tim/Autumn22_DFCCU/data/processed/maxar_subset_pm.csv"

df_bhm = pd.read_csv(csv_bhm)
df_maxar = pd.read_csv(csv_maxar)

# print(df_bhm.info())
# print(df_maxar.info())


df_bhm["file_code"] = df_bhm.file_name.str[:8].str.split("-").str.join("").astype(int)
df_maxar["file_code"] = (
    df_maxar.file_name.str[:8].str.split("_").str.join("").astype(int)
)

dfs = [df_bhm, df_maxar]
for df in dfs:
    df["pixel_err_x"] = np.abs(((df.right - df.left) / df.pixel_horiz) - 0.5)
    df["pixel_err_y"] = np.abs(((df.top - df.bottom) / df.pixel_vert) - 0.5)


if filter_criterion == "pixel_size":
    df_bhm = df_bhm.loc[
        (df_bhm["pixel_horiz"] > pixel_small) & (df_bhm["pixel_vert"] > pixel_small)
    ]
    df_maxar = df_maxar.loc[
        (df_maxar["pixel_horiz"] > pixel_small) & (df_maxar["pixel_vert"] > pixel_small)
    ]

else:
    df_bhm = df_bhm.loc[
        (df_bhm["pixel_err_x"] <= err_tol) & (df_bhm["pixel_err_y"] <= err_tol)
    ]
    df_maxar = df_maxar.loc[
        (df_maxar["pixel_err_x"] <= err_tol) & (df_maxar["pixel_err_y"] <= err_tol)
    ]

print(df_bhm.info())
print(df_maxar.info())

df_maxar = df_maxar.loc[df_maxar["file_code"].isin(df_bhm["file_code"].values)]
df_bhm = df_bhm.sort_values("file_code", ascending=True)
df_maxar = df_maxar.sort_values("file_code", ascending=True)

df_maxar = df_maxar.reset_index(drop=True)
df_bhm = df_bhm.reset_index(drop=True)

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

# make a directory for the new file pairs
datapath = "/home/tim/data/UNICEF_data/tim_maxar_bhm_final_pairs"

datapath_alt = "/home/tim/data/UNICEF_data"

# copy files in loop
# split this into chunks
chunk_size = 20
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
        print("folders exist")

    print("Zipping chunk", j, " / ", num_chunks)
    for k in range(chunk_sizes[j]):
        i = k + j * chunk_sizes[j]

        new_maxar_name = subpath + "/maxar/maxar-" + str(df_maxar.file_code[i]) + ".tif"
        old_maxar_name = (
            datapath_alt
            + "/kaggle_maxar_tiles_subset/data/maxar_tiles/"
            + df_maxar.file_name[i]
        )

        new_bhm_name = subpath + "/bhm/bhm-" + str(df_bhm.file_code[i]) + ".tif"
        old_bhm_name = (
            datapath_alt
            + "/height_model_subset/"
            + df_bhm.file_code[i][:4]
            + "-BHM/BHM-"
            + df_bhm.file_name[i]
            + ".tif"
        )

        shutil.copyfile(old_maxar_name, new_maxar_name)
        shutil.copyfile(old_bhm_name, new_bhm_name)

    # zip the files
    shutil.make_archive(datapath + "/maxar_bhm_pairs_" + str(j), "zip", subpath)
