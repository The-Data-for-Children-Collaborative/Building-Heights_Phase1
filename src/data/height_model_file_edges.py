# code Dana
""" write cvs-file with edge coordinate information (coordinate system:UTM, zone 23K) and pixel(vertical and horizontal) number for each building height tif file (non-merged)"""

# packages needed
import numpy as np
import glob
import rioxarray as rxr
import pandas as pd

#list height-model BH(building height) files, adaptet from list_BHM_files.py
# path to data
datapath = "/home/dana/data/UNICEF_data/height-model/"

# search through BHM folders and add them to list
folder_search = glob.glob(datapath + "????-BHM")
folder_list = []
for folder in folder_search:
    folder_list.append(folder)
file_list=[] 
for folder in folder_list:
    file_search = glob.glob(folder + "/BHM-????-???.tif")
    file_list.extend(file_search)

#extract data from hieght model files
x_min_list=[]
x_max_list=[]
pixel_x_list=[]
y_max_list=[]
y_min_list=[]
pixel_y_list=[]
file_name_list=[]
for file in file_list:
    file_array=rxr.open_rasterio(file)
    x_min_list.append(np.nanmin(file_array.x))
    x_max_list.append(np.nanmax(file_array.x))
    y_min_list.append(np.nanmin(file_array.y))
    y_max_list.append(np.nanmax(file_array.y))
    pixel_x_list.append(len(file_array.x))
    pixel_y_list.append(len(file_array.y))
    file_name_list.append(file[file.find(start:='BHM-')+len(start):file.find('.tif')])
    print(file,' data extracted')

#write to dataframe and save as csv file
hm_BH_df=pd.DataFrame({'file_name':file_name_list,
                       'left':x_min_list,
                       'right':x_max_list,
                       'top':y_max_list,
                       'bottom':y_min_list,
                       'pixel_horiz':pixel_x_list,
                       'pixel_vert':pixel_y_list})

print('dataframe created')
filepath="/home/dana/height_model_file_edges.csv"
hm_BH_df.to_csv(filepath,index=False)
print('data written to csv file, done!')
