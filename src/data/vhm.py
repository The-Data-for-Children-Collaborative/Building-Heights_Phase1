r"""Crop VHM files to same extents as BHM / maxar final pairs."""

from osgeo import gdal
import pandas as pd
import height_model_file_edges
import list_files
from os.path import expanduser, isfile
import subprocess
import regrid_maxar

### USER INPUTS ###
use_subset = False
overwrite_files = False

### END INPUTS  ###

# first write the list of VHM files
# get the home directory
homedir = expanduser("~")

# get the data path
datadir = homedir + "/data/"

# path to write csv summary files to
csvs_path = datadir + "UNICEF_data/summary_data/"

# path to write lists of files to
listfiles_path = csvs_path + "file_lists/"

# list the VHM files
if use_subset:
    VHM_init_path = datadir + "UNICEF_data/height_model_subset/"
    VHM_filename = "VHM_subset_raw_list.txt"
else:
    VHM_init_path = datadir + "UNICEF_data/height-model-copy/"
    VHM_filename = "VHM_raw_list.txt"

list_files.list_VHM_files(VHM_init_path, listfiles_path, VHM_filename)

# transform to EPSG 3857
regrid_maxar.reproject_all_bhm(listfiles_path + VHM_filename)


# list the reprojected files
if use_subset:
    VHM_filename = "VHM_subset_reproj_list.txt"
else:
    VHM_filename = "VHM_reproj_list.txt"
list_files.list_VHM_files(
    VHM_init_path, listfiles_path, VHM_filename, search_string="_reproject"
)


# first get the input and output csv
if use_subset:
    VHM_csv = "VHM_pm_subset.csv"
else:
    VHM_csv = "VHM_pm.csv"

# write the co-ordinates to csv
height_model_file_edges.write_csv(
    listfiles_path + VHM_filename, csvs_path + VHM_csv, bhm=False, vhm=True
)

# define the maxar csv file
if use_subset:
    maxar_csv = "maxar_subset_pm.csv"
else:
    maxar_csv = "maxar_pm.csv"

# project into maxar files (can it be done?)
regrid_maxar.reproject_vhm_all(
    VHM_init_path,
    VHM_init_path,
    csvs_path + maxar_csv,
    csvs_path + VHM_csv,
)

if use_subset:
    VHM_filename = "VHM_subset_reproj_res_list.txt"
    VHM_csv = "VHM_subset_pm_res.csv"
else:
    VHM_filename = "VHM_reproj_res_list.txt"
    VHM_csv = "VHM_pm_res.csv"

list_files.list_VHM_files(
    VHM_init_path, listfiles_path, VHM_filename, search_string="_reproject_resolve"
)

height_model_file_edges.write_csv(
    listfiles_path + VHM_filename, csvs_path + VHM_csv, bhm=False, vhm=True
)
