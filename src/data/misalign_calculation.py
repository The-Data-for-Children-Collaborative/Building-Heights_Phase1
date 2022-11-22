""" write cvs-file with matrix size, resolution, and pixel misalignment for files from 2 different foldes"""

# packages needed
import numpy as np
import pandas as pd
from osgeo import gdal
import PIL
from PIL import Image
import os
from fnmatch import fnmatch

### user information: ###

# The user should write: misalignment(folder_1_path, folder_2_path, output_dir_filename) 
# and add:
# folder_1_path = the directory of the folder 1 (containing set 1 of files).
# folder_2_path = the directory of the folder 2 (containing set 2 of files).
# output_dir_filename = the directory and file name to save the output csv with the results.
# the files have to be referenced with the numbers in the positions 4 to 11 (start counting at 0).
# (otherwise change lines 48,54 and 57 of this code).
# Example of how to run this function :
# misalignment("/home/jaume/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_10/bhm/", "/home/jaume/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_10/vhm/", "/home/jaume/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_10/vhm_bhm_misalignment.csv")
# Folder_1: /pairs_10/bhm
# Folder_2: /pairs_10/vhm
# The output is save as: /pairs_10/vhm_bhm_misalignment.csv

###   end of user information   ###

# function to activate code
def misalignment(folder_1_path,folder_2_path,output_dir_filename):

# create the lists
    list_path = []
    list_path1 = []
    files = []
    file1s = []
    file_names = []
    size_maxars = []
    size_lidars = []
    m_res_x_ys = []
    l_res_x_ys = []
    pixel_mis_xls = []
    pixel_mis_xrs = []
    pixel_mis_yus = []
    pixel_mis_yds = []
    pixel_mis_xs = []
    pixel_mis_ys = []
    

# loop to find the pairs of files with the same reference numbers  
    for dirname, _, filenames in os.walk(folder_1_path):
        for filename in filenames: 
            list_path.append(os.path.join(dirname, filename))
            files.append(filename)
            files1 = sorted(files, key = lambda x: x[4:12]) 

    for dirname1, _, filename1s in os.walk(folder_2_path):
        for filename1 in filename1s: 
            list_path1.append(os.path.join(dirname1, filename1))
            file1s.append(filename1)
            file1s1 = sorted(file1s, key = lambda x: x[4:12]) 

    for filename, filename1 in zip(files1, file1s1):
        if filename[4:12] == filename1[4:12]: 
            
            first_arg = os.path.join(folder_1_path, filename)
            second_arg = os.path.join(folder_2_path, filename1)
            first, sec = gdal.Open(first_arg), gdal.Open(second_arg)              

# Opening the data (Maxar image and Lidar raster)
            reproL = first
            reproM = sec
# To obtain the pixel size
            pixelM = reproM.GetGeoTransform()
            pixelL = reproL.GetGeoTransform()
# Finding number of rows and columns
            imgM = PIL.Image.open(second_arg)
            imgL = PIL.Image.open(first_arg)
            widM, hgtM = imgM.size
            widL, hgtL = imgL.size
# Finding co-ordinates Maxar image (UpperLeft: ulx,uly; LowerLeft: ulx,lry; UpperRight: lrx,uly; LowerRight: lrx,lry)
            srcM = reproM
            ulxM, xresM, xskewM, ulyM, yskewM, yresM  = srcM.GetGeoTransform()
            lrxM = ulxM + (srcM.RasterXSize * xresM)
            lryM = ulyM + (srcM.RasterYSize * yresM)
# Length of X and Y in co-ordinates for Maxar image
            Diff_coord_xM = lrxM -ulxM
            Diff_coord_yM = ulyM -lryM
# Correspondance in X and Y of number in co-ordinate for each pixel for Maxar image
            Coord_Pixel_xM = Diff_coord_xM/widM
            Coord_Pixel_yM = Diff_coord_yM/hgtM
# Finding co-ordinates Lidar images (UpperLeft: ulx,uly; LowerLeft: ulx,lry; UpperRight: lrx,uly; LowerRight: lrx,lry)
            srcL = reproL
            ulxL, xresL, xskewL, ulyL, yskewL, yresL  = srcL.GetGeoTransform()
            lrxL = ulxL + (srcL.RasterXSize * xresL)
            lryL = ulyL + (srcL.RasterYSize * yresL)
# Length of X and Y in co-ordinates for Lidar image
            Diff_coord_xL = lrxL -ulxL
            Diff_coord_yL = ulyL -lryL
# Correspondance in X and Y of number in co-ordinate for each pixel for Lidar image
            Coord_Pixel_xL = Diff_coord_xL/widL
            Coord_Pixel_yL = Diff_coord_yL/hgtL
# Pixel misaligned
            Xleft = (ulxM- ulxL)/Coord_Pixel_xM
            Xright = (lrxM- lrxL)/Coord_Pixel_xM
            Yup = np.abs((ulyM- ulyL)/Coord_Pixel_yM)
            Ylow = np.abs((lryM- lryL)/Coord_Pixel_yM)
# Calculations:
            size_maxar = str(widM),str(hgtM) # rows x columns
            size_lidar = str(widL), str(hgtL) # rows x columns
            m_res_x_y = round(pixelM[1],5), np.abs(round(pixelM[5],5)) # numero of pixels maxar (of file_2)
            l_res_x_y = round(pixelL[1],5), np.abs(round(pixelL[5],5)) # numero of pixels maxar (of file_1)
            pixel_mis_xl = round(Xleft,2) # Differences in X left co-ordinates (Maxar-Lidar) divided per the co-ordinate per pixel
            pixel_mis_xr = round(Xright,2) # Differences in X right co-ordinates (Maxar-Lidar) divided per the co-ordinate per pixel
            pixel_mis_yu = round(Yup,2) # Differences in Y up co-ordinates (Maxar-Lidar) divided per the co-ordinate per pixel
            pixel_mis_yd = round(Ylow,2) # Differences in Y low co-ordinates (Maxar-Lidar) divided per the co-ordinate per pixel
            pixel_mis_x = round(Xleft+Xright,2) # Sum of the X pixel differences
            pixel_mis_y = round(Yup+Ylow,2) # Sum of the Y pixel differences

# collect the results to be added to the lists                
            file_names.append(filename1[4:12])
            size_maxars.append(size_maxar)
            size_lidars.append(size_lidar)
            m_res_x_ys.append(m_res_x_y)
            l_res_x_ys.append(l_res_x_y)
            pixel_mis_xls.append(pixel_mis_xl)
            pixel_mis_xrs.append(pixel_mis_xr)
            pixel_mis_yus.append(pixel_mis_yu)
            pixel_mis_yds.append(pixel_mis_yd)
            pixel_mis_xs.append(pixel_mis_x)
            pixel_mis_ys.append(pixel_mis_y)
                    
# write to dataframe 
    misalign = pd.DataFrame(
        {"file_names": file_names,
         "size_folder_2": size_maxars,
         "size_folder_1": size_lidars,
         "folder_2_resolution_x,y": m_res_x_ys,
         "folder_1_resolution_x,y": l_res_x_ys,
         "Num_Pixel_misaligned_Xleft": pixel_mis_xls,
         "Num_Pixel_misaligned_Xright": pixel_mis_xrs,
         "Num_Pixel_misaligned_Yup": pixel_mis_yus,
         "Num_Pixel_misaligned_Ydown": pixel_mis_yds,
         "Pixel_Misaligned_X": pixel_mis_xs,
         "Pixel_Misaligned_Y": pixel_mis_ys})

# save the dataframe as csv file
    print("dataframe created")
    filepath = output_dir_filename
    misalign.to_csv(filepath, index=False)

# display the contents of the output csv
    print("The csv file written successfully and generated...")