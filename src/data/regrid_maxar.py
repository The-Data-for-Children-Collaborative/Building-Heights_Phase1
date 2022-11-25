"""
Regrid the maxar png files to match the BHM tif files.
"""

from osgeo import gdal
import pandas as pd
import height_model_file_edges
import list_files
from os.path import expanduser, isfile
import subprocess


def reproject_all_bhm(input_file_list, overwrite_files=False):
    """Reproject all the BHM files.

    Parameters
    ----------
    input_file_list : str
        name of file containing list of BHM files to reproject
    """
    with open(input_file_list, "r") as f:
        input_files = f.readlines()

    # loop over the files in the list
    for i, input_file in enumerate(input_files):
        print("Regridding BHM files", str(i + 1) + " / " + str(len(input_files)))
        output_file = input_file[:-5] + "_reproject.tif"
        if isfile(output_file) and not overwrite_files:
            continue
        gdal_reproject_bhm(input_file.strip(), output_file)
        subprocess.call(["chmod", "770", output_file])


def georef_crop_all_maxar(
    datapath_in, datapath_out, input_csv, grid_extent_csv, overwrite_files=False
):
    """Geo-reference the maxar png files and crop them to the BHM extents.

    Parameters
    ----------
    datapath_in : str
        input datapath for the maxar png files
    datapath_out : str
        output datapath for the georeferenced files
    input_csv : str
        maxar csv file
    grid_extent_csv : str
        grid extents for the maxar files
    """
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
        filename_out = datapath_out + filecode + "_reproject.tif"
        if isfile(filename_out) and not overwrite_files:
            continue
        if lrx - ulx <= 0:
            print("Skipping, negative x window")
        elif uly - lry <= 0:
            print("Skipping, negative y window")
        else:
            pixels = [row.pixel_horiz.values[0], row.pixel_vert.values[0]]

            # print(coords, filename, filename_out)
            gdal_georef_crop_maxar(filename, filename_out, coords_a, coords_b)
            subprocess.call(["chmod", "770", filename_out])


def resolve_bhm_all(
    datapath_in, datapath_out, maxar_csv, bhm_csv, overwrite_files=False
):
    """Change the resolution of BHM images to match maxar data.

    Parameters
    ----------
    datapath_in : str
        input datapath for the maxar png files
    datapath_out : str
        output datapath for the georeferenced files
    maxar_csv : str
        maxar csv file (cropped to bhm extents)
    bhm_csv : str
        bhm csv file (reprojected to epsg co-ords)
    """
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
        filename_out = (
            datapath_out + filecode[:4] + "-BHM/BHM-" + filecode + "_resolve.tif"
        )
        if isfile(filename_out) and not overwrite_files:
            continue
        if lrx - ulx <= 0:
            print("Skipping, negative x window")
        elif uly - lry <= 0:
            print("Skipping, negative y window")
        else:
            pixels = [row_alt.pixel_horiz.values[0], row_alt.pixel_vert.values[0]]
            gdal_resolve_bhm(filename, filename_out, coords, pixels)
            subprocess.call(["chmod", "770", filename_out])


def reproject_vhm_all(
    datapath_in, datapath_out, maxar_csv, vhm_csv, overwrite_files=False
):
    """Change the resolution of VHM images to match maxar data.

    Parameters
    ----------
    datapath_in : str
        input datapath for the maxar png files
    datapath_out : str
        output datapath for the georeferenced files
    maxar_csv : str
        maxar csv file (cropped to vhm extents)
    vhm_csv : str
        vhm csv file (reprojected to epsg co-ords)
    """
    # read in the csv file
    maxar_df = pd.read_csv(maxar_csv)

    # read the VHM csv file
    vhm_df = pd.read_csv(vhm_csv)

    # loop over the csv
    for i in range(len(vhm_df)):
        print("Changing resolution of VHM files", str(i + 1) + " / " + str(len(vhm_df)))
        row = vhm_df.loc[[i]]
        filecode = row.file_name.values[0]
        search_string = "_".join(filecode[:8].split("-"))
        subcode = filecode.split("-")[0]
        row_alt = maxar_df[maxar_df.file_name.str.contains(search_string)]
        # row_alt = maxar_df.loc[[i]]
        filename = datapath_in + subcode + "-VHM/VHM-" + filecode + ".tif"
        try:
            ulx = row_alt.left.values[0]
            uly = row_alt.top.values[0]
            lrx = row_alt.right.values[0]
            lry = row_alt.bottom.values[0]
            if (
                ulx < row.left.values[0]
                or uly > row_alt.top.values[0]
                or lrx > row.right.values[0]
                or lry < row.bottom.values[0]
            ):
                print("Potential problem in file ", filecode)
        except IndexError:
            continue
        coords = [ulx, uly, lrx, lry]
        filename_out = (
            datapath_out + filecode[:4] + "-VHM/VHM-" + filecode + "_resolve.tif"
        )
        if isfile(filename_out) and not overwrite_files:
            continue
        if lrx - ulx <= 0:
            print("Skipping, negative x window")
        elif uly - lry <= 0:
            print("Skipping, negative y window")
        else:
            pixels = [row_alt.pixel_horiz.values[0], row_alt.pixel_vert.values[0]]
            gdal_resolve_bhm(filename, filename_out, coords, pixels)
            subprocess.call(["chmod", "770", filename_out])


def gdal_reproject_bhm(input_filename, output_filename):
    """Change BHM file to EPSG:3857 reference.

    Parameters
    ----------
    input_filename : str
        name of the input file
    output_filename : str
        name of the output file
    """
    gdal.Warp(output_filename, input_filename, dstSRS="EPSG:3857")


def gdal_resolve_bhm(input_filename, output_filename, coords, pixels):
    """Resolve BHM file to speficic pixellation.

    Parameters
    ----------
    input_filename : str
        name of the input file
    output_filename : str
        name of the output file
    coords : list of floats
        co-ords [x0, y1, x1, y0] of projection window
    pixels : list of ints
        [x, y] pixels to resolve into
    """
    gdal.Translate(
        output_filename,
        input_filename,
        options="-projwin "
        + " ".join([str(c) for c in coords])
        + " -outsize "
        + " ".join([str(p) for p in pixels]),
    )


def gdal_georef_crop_maxar(input_filename, output_filename, coords_in, coords_out):
    """Resolve BHM file to speficic pixellation.

    Parameters
    ----------
    input_filename : str
        name of the input file
    output_filename : str
        name of the output file
    coords_in : list of floats
        co-ords [x0, y1, x1, y0] corresponding to the input png file
    coords_out : list of floats
        co-ords [x0, y1, x1, y0] corresponding to the output projection window.
    """
    gdal.Translate(
        "tmpgdal.png",
        input_filename,
        options="-a_srs EPSG:3857 -a_ullr " + " ".join([str(c) for c in coords_in]),
    )

    gdal.Translate(
        output_filename,
        "tmpgdal.png",
        options="-of GTiff -projwin " + " ".join([str(c) for c in coords_out]),
    )
    return


def _tf_from_yn(yn):
    """Return True / False based on y/n input."""
    if yn == "y":
        return True
    else:
        return False


if __name__ == "__main__":

    # get the home directory
    homedir = expanduser("~")

    # get the data path
    datadir = homedir + "/data/"

    # user input about which parts of pipeline to run
    use_default_datadir = _tf_from_yn(
        input("Use default data directory (" + datadir + ")? [y/n] ")
    )
    if not use_default_datadir:
        datadir = input("Please enter the path to the S3 data bucket: ")
    use_subset = _tf_from_yn(
        input("Use subset of data (y) or full dataset (n)? [y/n] ")
    )
    convert_BHM = _tf_from_yn(input("Convert BHM co-ordinates to epsg:3857? [y/n] "))
    convert_maxar = _tf_from_yn(input("Crop maxar images to BHM extents? [y/n] "))
    resolve_BHM_pixels = _tf_from_yn(input("Downsample BHM to maxar size? [y/n] "))
    overwrite_files = _tf_from_yn(input("Re-run already processed files? [y/n] "))

    # check if subset is False
    if not use_subset:
        choice = input("Are you sure you want to run on the full dataset? [y/n]")
        if choice == "n":
            use_subset = True

    # path to write csv summary files to
    csvs_path = datadir + "UNICEF_data/summary_data/"

    # path to write lists of files to
    listfiles_path = csvs_path + "file_lists/"

    # write BHM files to list
    if use_subset:
        BHM_init_path = datadir + "UNICEF_data/height_model_subset/"
        BHM_filename = "BHM_subset_raw_list.txt"
    else:
        BHM_init_path = datadir + "UNICEF_data/height-model-copy/"
        BHM_filename = "BHM_raw_list.txt"

    if convert_BHM:
        list_files.list_BHM_files(BHM_init_path, listfiles_path, BHM_filename)
        reproject_all_bhm(listfiles_path + BHM_filename, overwrite_files)

    if use_subset:
        BHM_filename = "BHM_subset_reproj_list.txt"
    else:
        BHM_filename = "BHM_subset_reproj_list.txt"

    list_files.list_BHM_files(
        BHM_init_path, listfiles_path, BHM_filename, search_string="_reproject"
    )

    # first get the input and output csv
    if use_subset:
        BHM_csv = "BHM_pm_subset.csv"
    else:
        BHM_csv = "BHM_pm.csv"

    height_model_file_edges.write_csv(
        listfiles_path + BHM_filename, csvs_path + BHM_csv
    )

    if use_subset:
        maxar_extent_file = datadir + "UNICEF_data/grids_extent.csv"
        datapath_in = (
            datadir + "UNICEF_data/kaggle_maxar_tiles_subset/data/maxar_tiles/"
        )
        datapath_out = (
            datadir + "UNICEF_data/kaggle_maxar_tiles_subset/data/maxar_tiles/"
        )
    else:
        maxar_extent_file = datadir + "/UNICEF_data/grids_extent.csv"
        datapath_in = datadir + "UNICEF_data/kaggle_maxar_tiles/data/maxar_tiles/"
        datapath_out = datadir + "UNICEF_data/kaggle_maxar_tiles_copy/data/maxar_tiles/"

    if convert_maxar:
        georef_crop_all_maxar(
            datapath_in,
            datapath_out,
            csvs_path + BHM_csv,
            maxar_extent_file,
            overwrite_files,
        )

    if use_subset:
        maxar_filename = "maxar_subset_list.txt"
        maxar_csv = "maxar_subset_pm.csv"
    else:
        maxar_filename = "maxar_list.txt"
        maxar_csv = "maxar_pm.csv"

    list_files.list_maxar_files(datapath_out, listfiles_path, maxar_filename)

    height_model_file_edges.write_csv(
        listfiles_path + maxar_filename, csvs_path + maxar_csv, bhm=False
    )

    if resolve_BHM_pixels:
        resolve_bhm_all(
            BHM_init_path,
            BHM_init_path,
            csvs_path + maxar_csv,
            csvs_path + BHM_csv,
            overwrite_files,
        )

    if use_subset:
        BHM_filename = "BHM_subset_reproj_res_list.txt"
        BHM_csv = "BHM_subset_pm_res.csv"
    else:
        BHM_filename = "BHM_subset_reproj_res_list.txt"
        BHM_csv = "BHM_pm_res.csv"

    list_files.list_BHM_files(
        BHM_init_path, listfiles_path, BHM_filename, search_string="_reproject_resolve"
    )

    height_model_file_edges.write_csv(
        listfiles_path + BHM_filename,
        csvs_path + BHM_csv,
    )
