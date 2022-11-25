"""
List all the BHM (non-merged) files from the AWS data folder.
"""

# file imports
import glob
import os

# get the current working directory
cwd = os.getcwd()


def list_BHM_files(datapath, writepath, filename_out, search_string=""):

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


def list_VHM_files(datapath, writepath, filename_out, search_string=""):

    # search through BHM folders and add them to list
    folder_search = glob.glob(datapath + "????-VHM")
    folder_list = []
    for folder in folder_search:
        folder_list.append(folder)

    # search through files and write them to file
    with open(writepath + filename_out, "w") as f:
        for folder in folder_list:
            file_search = glob.glob(folder + "/VHM-????-???" + search_string + ".tif")
            for file in file_search:
                f.write(file + "\n")


def list_maxar_files(datapath, writepath, filename_out):

    # search through files and write them to file
    with open(writepath + filename_out, "w") as f:
        file_search = glob.glob(datapath + "*_reproject.tif")
        for file in file_search:
            f.write(file + "\n")
