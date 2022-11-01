"""
Regrid the maxar png files to match the BHM tif files.
"""

import sys
from osgeo import gdal
import shutil
import pandas as pd
import height_model_file_edges
import list_maxar_tifs

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


def maxar_to_tif_all(datapath_in, datapath_out, input_csv, grid_extent_csv):

    # read in the csv file
    maxar_csv = pd.read_csv(input_csv)

    # read the other csv file
    grid_extent_csv = pd.read_csv(grid_extent_csv)

    # loop over the csv
    for i in range(len(maxar_csv)):
        print(str(i + 1) + " / " + str(len(maxar_csv)))
        row = maxar_csv.loc[[i]]
        filecode = "_".join(row.file_name.values[0].split("-"))[:8]
        filecode_alt = "-".join(filecode.split("_"))
        row_alt = grid_extent_csv.loc[grid_extent_csv["qmdt_cod"] == filecode_alt]
        filename = datapath_in + filecode + ".png"
        ulx = row_alt.left.values[0]
        uly = row_alt.top.values[0]
        lrx = row_alt.right.values[0]
        lry = row_alt.bottom.values[0]
        coords_a = [ulx, uly, lrx, lry]
        ulx = max(row.left.values[0], row_alt.left.values[0])
        uly = min(row.top.values[0], row_alt.top.values[0])
        lrx = min(row.right.values[0], row_alt.right.values[0])
        lry = max(row.bottom.values[0], row_alt.bottom.values[0])
        coords_b = [ulx, uly, lrx, lry]
        pixels = [row.pixel_horiz.values[0], row.pixel_vert.values[0]]
        filename_out = datapath_out + filecode + "_reproject.tif"
        # print(coords, filename, filename_out)
        maxar_to_tif(filename, filename_out, coords_a, coords_b, pixels)

    return


def resolve_BHM_all(datapath_in, datapath_out, maxar_csv, bhm_csv):

    # read in the csv file
    maxar_df = pd.read_csv(maxar_csv)

    # read the BHM csv file
    bhm_df = pd.read_csv(bhm_csv)

    # loop over the csv
    for i in range(len(maxar_df)):
        print(str(i + 1) + " / " + str(len(maxar_df)))
        row = bhm_df.loc[[i]]
        filecode = row.file_name.values[0]
        subcode = filecode.split("-")[0]
        row_alt = maxar_df.loc[[i]]
        filename = datapath_in + subcode + "-BHM/BHM-" + filecode + ".tif"
        ulx = max(row_alt.left.values[0], row.left.values[0])
        uly = min(row.top.values[0], row_alt.top.values[0])
        lrx = min(row.right.values[0], row_alt.right.values[0])
        lry = max(row.bottom.values[0], row_alt.bottom.values[0])
        coords = [ulx, uly, lrx, lry]
        pixels = [row_alt.pixel_horiz.values[0], row_alt.pixel_vert.values[0]]
        filename_out = datapath_out + "BHM-" + filecode + "_resolve.tif"
        resolve_BHM(filename, filename_out, coords, pixels)

    return


def reproject_BHM(input_filename, output_filename):
    ds_repro = gdal.Warp(
        output_filename,
        input_filename,
        dstSRS="EPSG:3857",
    )
    return


def resolve_BHM(input_filename, output_filename, coords, pixels):

    ds_repro = gdal.Translate(
        output_filename,
        input_filename,
        options="-projwin "
        + " ".join([str(c) for c in coords])
        + " -outsize "
        + " ".join([str(p) for p in pixels]),
    )

    return


def maxar_to_tif(input_filename, output_filename, coords_a, coords_b, pixels):
    ds_repro = gdal.Translate(
        "tmpgdal.png",
        input_filename,
        options="-a_srs EPSG:3857 -a_ullr " + " ".join([str(c) for c in coords_a]),
    )

    ds_repro = gdal.Translate(
        output_filename,
        "tmpgdal.png",
        options="-of GTiff -projwin " + " ".join([str(c) for c in coords_b]),
    )
    return


if __name__ == "__main__":
    # input_filename = "/home/tim/data/UNICEF_data/height-model/2222-BHM/BHM-2222-132.tif"
    # output_filename = (
    #    "/home/tim/Autumn22_DFCCU/data/raw/2222-BHM/BHM-2222-132_reprojected.tif"
    # )
    # output_filename_2 = (
    #    "/home/tim/data/UNICEF_data/height-model/2222-BHM/BHM-2222-132_reprojected.tif"
    # )

    # reproject_all_BHM(
    #     "/home/tim/Autumn22_DFCCU/data/processed/BHM_file_list_subset.txt"
    # )

    datapath_in = "/home/tim/data/UNICEF_data/kaggle_maxar_tiles_copy/data/maxar_tiles/"
    datapath_out = (
        "/home/tim/data/UNICEF_data/kaggle_maxar_tiles_copy/data/maxar_tiles/"
    )

    # first get the input and output csv
    height_model_file_edges.write_csv(
        "/home/tim/Autumn22_DFCCU/data/processed/BHM_file_list.txt",
        "/home/tim/data/BHM_pm.csv",
    )

    maxar_to_tif_all(
        datapath_in,
        datapath_out,
        "/home/tim/data/BHM_pm.csv",
        "/home/tim/data/UNICEF_data/grids_extent_subset.csv",
    )

    datapath_in = "/home/tim/data/UNICEF_data/height-model-copy/"
    datapath_out = "/home/tim/data/UNICEF_data/height-model-copy/"

    list_maxar_tifs.write_files(
        "/home/tim/data/UNICEF_data/kaggle_maxar_tiles_copy/data/maxar_tiles/"
    )

    height_model_file_edges.write_csv(
        "/home/tim/Autumn22_DFCCU/data/processed/maxar_file_list.txt",
        "/home/tim/data/maxar_pm.csv",
    )

    resolve_BHM_all(
        datapath_in,
        datapath_out,
        "/home/tim/data/maxar_pm.csv",
        "/home/tim/data/BHM_pm.csv",
    )
