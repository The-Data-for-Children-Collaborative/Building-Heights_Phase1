import pandas as pd
import numpy as np
import os
import shutil

# error tolerance
err_tol = 0.005
pixel_base = 0.5


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

df_bhm = df_bhm.loc[
    (df_bhm["pixel_err_x"] <= err_tol) & (df_bhm["pixel_err_y"] <= err_tol)
]
df_maxar = df_maxar.loc[
    (df_maxar["pixel_err_x"] <= err_tol) & (df_maxar["pixel_err_y"] <= err_tol)
]


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
datapath = "/home/tim/data/UNICEF_data/"

try:
    os.makedirs(datapath + "/tmp_pairs")
    os.makedirs(datapath + "/tmp_pairs/maxar")
    os.makedirs(datapath + "/tmp_pairs/bhm")
except FileExistsError:
    print("folders exist")

datapath_alt = "/home/tim/data/UNICEF_data"

# copy files in loop
for i in range(len(df_maxar)):
    new_maxar_name = (
        datapath + "/tmp_pairs/maxar/maxar-" + str(df_maxar.file_code[i]) + ".tif"
    )
    old_maxar_name = (
        datapath_alt
        + "/kaggle_maxar_tiles_subset/data/maxar_tiles/"
        + df_maxar.file_name[i]
    )

    new_bhm_name = datapath + "/tmp_pairs/bhm/bhm-" + str(df_bhm.file_code[i]) + ".tif"
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
shutil.make_archive(datapath + "/maxar_bhm_pairs", "zip", datapath + "/tmp_pairs")

# delete the directory
shutil.rmtree(datapath + "/tmp_pairs")
