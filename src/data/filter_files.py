import pandas as pd
import numpy as np

# error tolerance
err_tol = 0.005
pixel_base = 0.5


# csv_bhm = "/home/tim/data/UNICEF_data/summary_data/BHM_subset_pm_res.csv"
# csv_maxar = "/home/tim/data/UNICEF_data/summary_data/maxar_subset_pm.csv"

csv_bhm = "/home/tim/Autumn22_DFCCU/data/processed/BHM_subset_pm_res.csv"
csv_maxar = "/home/tim/Autumn22_DFCCU/data/processed/maxar_subset_pm.csv"

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

print(df_bhm.tail())
print(df_maxar.tail())


df_bhm.file_code = (
    df_bhm.file_code.astype("str").str[:4]
    + "-"
    + df_bhm.file_code.astype("str").str[4:]
)

print(df_bhm.head())
