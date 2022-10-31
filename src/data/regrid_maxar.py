"""
Regrid the maxar png files to match the BHM tif files.
"""

import sys
from osgeo import gdal
import shutil
import pandas as pd

# username
try:
    username = sys.argv[1]
except IndexError:
    sys.exit("Please enter username as command line arg")

# list height-model BH(building height) files, adaptet from list_BHM_files.py
# path to data
datapath = "/home/" + username + "/data/UNICEF_data/height-model/"
path = "/home/tim/data"


def reproject_all_BHM(input_file_list):

    with open(input_file_list, "r") as f:
        input_files = f.readlines()

    # loop over the files in the list
    for i, input_file in enumerate(input_files):
        print(str(i + 1) + " / " + str(len(input_files)))
        output_file = input_file[:-5] + "_reproject.tif"
        reproject_BHM(input_file.strip(), output_file)

    return


def maxar_to_tif_all(datapath, input_csv):

    # read in the csv file
    maxar_csv = pd.read_csv(input_csv)

    # loop over the csv
    for i in range(10):
        row = maxar_csv.loc[[i]]
        filecode = "_".join(row.qmdt_cod.values[0].split("-"))
        filename = datapath + filecode + ".png"
        ulx = row.left.values[0]
        uly = row.top.values[0]
        lrx = row.right.values[0]
        lry = row.bottom.values[0]
        coords = [ulx, uly, lrx, lry]
        filename_out = datapath + filecode + ".tif"
        print(coords, filename, filename_out)
        # maxar_to_tif(filename, filename_out, coords)

    return


def reproject_BHM(input_filename, output_filename):
    ds_repro = gdal.Translate(
        output_filename,
        input_filename,
        options="-a_srs EPSG:3857",
    )
    return


def maxar_to_tif(input_filename, output_filename, coords):
    ds_repro = gdal.Translate(
        "input_filename",
        "output_filename",
        options="-a_srs EPSG:3857 -a_ullr" + " ".join(coords),
    )
    return


if __name__ == "__main__":
    input_filename = "/home/tim/data/UNICEF_data/height-model/2222-BHM/BHM-2222-132.tif"
    output_filename = (
        "/home/tim/Autumn22_DFCCU/data/raw/2222-BHM/BHM-2222-132_reprojected.tif"
    )
    output_filename_2 = (
        "/home/tim/data/UNICEF_data/height-model/2222-BHM/BHM-2222-132_reprojected.tif"
    )

    reproject_all_BHM("/home/tim/Autumn22_DFCCU/data/processed/BHM_file_list.txt")

    datapath = "/home/tim/data/UNICEF_data/kaggle_maxar_tiles/data/maxar_tiles/"
    # maxar_to_tif_all(datapath, "/home/tim/data/UNICEF_data/grids_extent.csv")
