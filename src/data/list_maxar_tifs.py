"""
65;6800;1cList all the BHM (non-merged) files from the AWS data folder.
"""

# file imports
import glob
import os


def write_files(datapath, filename_out):

    # get the current working directory
    cwd = os.getcwd()

    # path to data: must change depending on username!
    # datapath = "/home/tim/data/UNICEF_data/kaggle_maxar_tiles_copy/data/maxar_tiles/"
    # datapath = "/home/tim/Autumn22_DFCCU/data/raw/"

    # path to write file to (no need to change)
    writepath = "/".join(cwd.split("/")[:4]) + "/data/processed/"

    # search through files and write them to file
    with open(writepath + filename_out, "w") as f:
        file_search = glob.glob(datapath + "*_reproject.tif")
        for file in file_search:
            f.write(file + "\n")

    return
