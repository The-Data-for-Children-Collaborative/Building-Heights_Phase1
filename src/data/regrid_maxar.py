"""
Regrid the maxar png files to match the BHM tif files.
"""

import sys
from osgeo import gdal
import shutil
import pandas as pd
import height_model_file_edges
import list_maxar_tifs
import list_BHM_files
from os.path import expanduser


def reproject_all_BHM(input_file_list):

    with open(input_file_list, "r") as f:
        input_files = f.readlines()

    # loop over the files in the list
    for i, input_file in enumerate(input_files):
        print("Regridding BHM files", str(i + 1) + " / " + str(len(input_files)))
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
        print(
            "Regridding and cropping maxar files",
            str(i + 1) + " / " + str(len(maxar_csv)),
        )
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
        if lrx - ulx <= 0:
            print("Skipping, negative x window")
        elif uly - lry <= 0:
            print("Skipping, negative y window")
        else:
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
    for i in range(len(bhm_df)):
        print("Changing resolution of BHM files", str(i + 1) + " / " + str(len(bhm_df)))
        row = bhm_df.loc[[i]]
        filecode = row.file_name.values[0]
        search_string = "_".join(filecode[:8].split("-"))
        subcode = filecode.split("-")[0]
        row_alt = maxar_df[maxar_df.file_name.str.contains(search_string)]
        # row_alt = maxar_df.loc[[i]]
        filename = datapath_in + subcode + "-BHM/BHM-" + filecode + ".tif"
        try:
            ulx = max(row.left.values[0], row_alt.left.values[0])
            uly = min(row.top.values[0], row_alt.top.values[0])
            lrx = min(row.right.values[0], row_alt.right.values[0])
            lry = max(row.bottom.values[0], row_alt.bottom.values[0])
        except IndexError:
            continue
        coords = [ulx, uly, lrx, lry]
        if lrx - ulx <= 0:
            print("Skipping, negative x window")
        elif uly - lry <= 0:
            print("Skipping, negative y window")
        else:
            pixels = [row_alt.pixel_horiz.values[0], row_alt.pixel_vert.values[0]]
            filename_out = (
                datapath_out + filecode[:4] + "-BHM/BHM-" + filecode + "_resolve.tif"
            )
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


def tf_from_yn(yn):

    if yn == "y":
        return True
    else:
        return False


if __name__ == "__main__":

    # user input about which parts of pipeline to run
    use_subset = tf_from_yn(input("Use subset of data (y) or full dataset (n)? [y/n] "))
    convert_BHM = tf_from_yn(input("Convert BHM co-ordinates to epsg:3857? [y/n] "))
    convert_maxar = tf_from_yn(input("Crop maxar images to BHM extents? [y/n] "))
    resolve_BHM_pixels = tf_from_yn(input("Downsample BHM to maxar size? [y/n] "))

    # check if subset is False
    if not use_subset:
        choice = input("Are you sure you want to run on the full dataset? [y/n]")
        if choice == "n":
            use_subset = True

    # get the home directory
    homedir = expanduser("~")

    # path to write lists of files to
    listfiles_path = homedir + "/Autumn22_DFCCU/data/processed/"

    # path to write csvs to
    csvfiles_path = homedir + "/data/"

    # write BHM files to list
    if use_subset:
        BHM_init_path = homedir + "/data/UNICEF_data/height_model_subset/"
        BHM_filename = "BHM_subset_raw_list.txt"
    else:
        BHM_init_path = homedir + "/data/UNICEF_data/height-model-copy/"
        BHM_filename = "BHM_raw_list.txt"

    if convert_BHM:
        list_BHM_files.write_files(BHM_init_path, BHM_filename)
        reproject_all_BHM(listfiles_path + BHM_filename)

    if use_subset:
        BHM_filename = "BHM_subset_reproj_list.txt"
    else:
        BHM_filename = "BHM_subset_reproj_list.txt"

    list_BHM_files.write_files(BHM_init_path, BHM_filename, search_string="_reproject")

    # first get the input and output csv
    if use_subset:
        BHM_csv = "BHM_pm_subset.csv"
    else:
        BHM_csv = "BHM_pm.csv"

    height_model_file_edges.write_csv(
        listfiles_path + BHM_filename, csvfiles_path + BHM_csv
    )

    if use_subset:
        maxar_extent_file = homedir + "/data/UNICEF_data/grids_extent.csv"
        datapath_in = (
            homedir + "/data/UNICEF_data/kaggle_maxar_tiles_subset/data/maxar_tiles/"
        )
        datapath_out = (
            homedir + "/data/UNICEF_data/kaggle_maxar_tiles_subset/data/maxar_tiles/"
        )
    else:
        maxar_extent_file = homedir + "/data/UNICEF_data/grids_extent.csv"
        datapath_in = homedir + "/data/UNICEF_data/kaggle_maxar_tiles/data/maxar_tiles/"
        datapath_out = (
            homedir + "/data/UNICEF_data/kaggle_maxar_tiles_copy/data/maxar_tiles/"
        )

    if convert_maxar:
        maxar_to_tif_all(
            datapath_in,
            datapath_out,
            csvfiles_path + BHM_csv,
            maxar_extent_file,
        )

    if use_subset:
        maxar_filename = "maxar_subset_list.txt"
        maxar_csv = "maxar_subset_pm.csv"
    else:
        maxar_filename = "maxar_list.txt"
        maxar_csv = "maxar_pm.csv"

    list_maxar_tifs.write_files(datapath_out, maxar_filename)

    height_model_file_edges.write_csv(
        listfiles_path + maxar_filename,
        csvfiles_path + maxar_csv,
    )

    if resolve_BHM_pixels:
        resolve_BHM_all(
            BHM_init_path,
            BHM_init_path,
            csvfiles_path + maxar_csv,
            csvfiles_path + BHM_csv,
        )

    if use_subset:
        BHM_filename = "BHM_subset_reproj_res_list.txt"
        BHM_csv = "BHM_subset_pm_res.csv"
    else:
        BHM_filename = "BHM_subset_reproj_res_list.txt"

    list_BHM_files.write_files(
        BHM_init_path, BHM_filename, search_string="_reproject_resolve"
    )

    height_model_file_edges.write_csv(
        listfiles_path + BHM_filename,
        csvfiles_path + BHM_csv,
    )
