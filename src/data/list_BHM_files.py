"""
List all the BHM (non-merged) files from the AWS data folder.
"""

# file imports
import glob
import os

# get the current working directory
cwd = os.getcwd()

# path to data: must change depending on username!
datapath = "/home/tim/data/UNICEF_data/height-model-copy/"
# datapath = "/home/tim/Autumn22_DFCCU/data/raw/"

# path to write file to (no need to change)
writepath = "/".join(cwd.split("/")[:4]) + "/data/processed/"


# search through BHM folders and add them to list
folder_search = glob.glob(datapath + "????-BHM")
folder_list = []
for folder in folder_search:
    folder_list.append(folder)

# search through files and write them to file
with open(writepath + "BHM_file_list.txt", "w") as f:
    for folder in folder_list:
        file_search = glob.glob(folder + "/BHM-????-???.tif")
        for file in file_search:
            f.write(file + "\n")
