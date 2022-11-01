# code Dana
""" write cvs-file with edge coordinate information (coordinate system:UTM, zone 23K) and pixel(vertical and horizontal) number for each building height tif file (non-merged)"""

# packages needed
import numpy as np
import glob
import rioxarray as rxr
import pandas as pd
import os.path
import sys

### user information: MUST EDIT ###

# output_file = "/home/tim/data/BHM_subset_pm_res.csv"
# input_file = "/home/tim/Autumn22_DFCCU/data/processed/BHM_file_list_subset_res.txt"

###   end of user information   ###


def write_csv(input_file, output_file):

    # read in file list from input file
    with open(input_file, "r") as f:
        file_list = f.readlines()

    # extract data from hieght model files
    x_min_list = []
    x_max_list = []
    pixel_x_list = []
    y_max_list = []
    y_min_list = []
    min_value_list = []
    max_value_list = []
    pixel_y_list = []
    file_name_list = []
    for file in file_list:
        file_array = rxr.open_rasterio(file.strip())
        x_min_list.append(np.nanmin(file_array.x))
        x_max_list.append(np.nanmax(file_array.x))
        y_min_list.append(np.nanmin(file_array.y))
        y_max_list.append(np.nanmax(file_array.y))
        pixel_x_list.append(len(file_array.x))
        pixel_y_list.append(len(file_array.y))
        min_value_list.append(np.nanmin(file_array))
        max_value_list.append(np.nanmax(file_array))
        file_name_list.append(
            file[file.find(start := "BHM-") + len(start) : file.find(".tif")]
        )
        print(file, " data extracted")

    # write to dataframe and save as csv file
    hm_BH_df = pd.DataFrame(
        {
            "file_name": file_name_list,
            "left": x_min_list,
            "right": x_max_list,
            "top": y_max_list,
            "bottom": y_min_list,
            "min_value": min_value_list,
            "max_value": max_value_list,
            "pixel_horiz": pixel_x_list,
            "pixel_vert": pixel_y_list,
        }
    )

    print("dataframe created")
    filepath = output_file
    hm_BH_df.to_csv(filepath, index=False)
    print("data written to csv file, done!")
