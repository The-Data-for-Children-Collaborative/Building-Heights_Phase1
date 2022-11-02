"""
List all the BHM (non-merged) files from the AWS data folder.
"""

# file imports
import glob
import os

# get the current working directory
cwd = os.getcwd()


def write_files(datapath, filename_out, search_string=""):

    # path to write file to (no need to change)
    writepath = "/".join(cwd.split("/")[:4]) + "/data/processed/"

    # search through BHM folders and add them to list
    folder_search = glob.glob(datapath + "????-BHM")
    folder_list = []
    for folder in folder_search:
        folder_list.append(folder)

    # search through files and write them to file
    with open(writepath + filename_out, "w") as f:
        for folder in folder_list:
            file_search = glob.glob(folder + "/BHM-????-???" + search_string + ".tif")
            for file in file_search:
                f.write(file + "\n")
