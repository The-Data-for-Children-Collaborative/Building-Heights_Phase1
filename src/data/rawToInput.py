"""
From raw to input data: make pairs of maxar png files and BHM tifs
"""

"""
BEFORE running the script: 

1) The name of the maxar images must be the same as the qmdt_cod in the csv file

2) Create the output folders:
maxar_georef
output_BHM
xyz
shp_2d
cropped_maxar

3) Change the paths for input and output data to match your local paths

4) Work with a copy of your original data. The filtering in step 2 permanently deletes the BHM reprojected files that are smaller than 100x100. This action is not taken in the raw data, it affects only the output of reprojection.

"""

# Define the path for the following directories

# Input data directories

grid_extent = "/Users/konstantinamitsi/Documents/S2DS/DFCCU/maxarBHMpairs/grids_extent.csv"
input_maxar_data = "/Users/konstantinamitsi/Documents/S2DS/DFCCU/maxarBHMpairs/maxar/"
input_BHM_data = "/Users/konstantinamitsi/Documents/S2DS/DFCCU/maxarBHMpairs/BHM/"

# Output data directories

output_maxar_data = "/Users/konstantinamitsi/Documents/S2DS/DFCCU/maxarBHMpairs/maxar_georef/"
output_BHM_data = "/Users/konstantinamitsi/Documents/S2DS/DFCCU/maxarBHMpairs/output_BHM/"
xyz_data = "/Users/konstantinamitsi/Documents/S2DS/DFCCU/maxarBHMpairs/xyz_test/"
shp_2d = "/Users/konstantinamitsi/Documents/S2DS/DFCCU/maxarBHMpairs/shp_2d/"
cropped_maxar = "/Users/konstantinamitsi/Documents/S2DS/DFCCU/maxarBHMpairs/cropped_maxar/"


# Import packages

from osgeo import gdal
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import fiona
import rasterio
import rasterio.mask
from os.path import exists as file_exists


# Read grid_extent into a dataframe

grid_extent = pd.read_csv(grid_extent)

# Step 1: Georeference the png maxar data using the grid_extent.csv file

for code in grid_extent["qmdt_cod"]:
    
    if file_exists(input_maxar_data + code + ".png"):
        
        left = grid_extent.loc[grid_extent["qmdt_cod"] == code, 'left'].item()
        top = grid_extent.loc[grid_extent["qmdt_cod"] == code, 'top'].item()
        right = grid_extent.loc[grid_extent["qmdt_cod"] == code, 'right'].item()
        bottom = grid_extent.loc[grid_extent["qmdt_cod"] == code, 'bottom'].item()
        projWin = [left, top, right, bottom]
        maxar_in = input_maxar_data + code + ".png"
        maxar_out = output_maxar_data + code + "_georef.tif"

        gdal.Translate(maxar_out, maxar_in, format = 'GTiff', outputSRS = 'EPSG:3857', outputBounds = projWin) 
        
        
    
    else: 
        print(code+'.png was not found in maxar input file')




# Step 2: Reproject BHM.tif files from EPSG:31983 to EPSG:3857

for path, currentDirectory, files in os.walk(input_BHM_data):
    for file in files:
        if file.endswith('.tif'):
            input_BHM = os.path.join(path, file)
            output_BHM = output_BHM_data+os.path.basename(input_BHM).split('.')[0]+"_reprojected.tif"
            gdal.Warp(output_BHM,input_BHM, dstSRS='EPSG:3857')
        
        else:
            print(file+'is not a tif')

# Filter BHM files with dimensions less than 100x100

for code in grid_extent["qmdt_cod"]:
    
    if file_exists(output_BHM_data + "BHM-" + code + "_reprojected.tif"): 
            rds = gdal.Open(output_BHM_data + "BHM-" + code + "_reprojected.tif")
            img_width = rds.RasterYSize
            img_height = rds.RasterXSize
            if img_width > 100 and img_height > 100:
                rds = None
            else:
                print("BHM-" + code + "_reprojected.tif fails filter")
                os.remove(output_BHM_data + "BHM-" + code + "_reprojected.tif")
    else: 
        pass
            

# Step 3: Crop the maxar data using the BHM data

# a) Extract the  geometry of the raster BHM_reprojected.tif files as point shapefiles

for code in grid_extent["qmdt_cod"]:
    
    if file_exists(output_BHM_data + "BHM-" + code + "_reprojected.tif"): 
        
        BHM_in = output_BHM_data + "BHM-" + code + "_reprojected.tif"
        xyz_out = xyz_data + code + ".xyz"
        
        # Transform the tif to xyz
        gdal.Translate(xyz_out, BHM_in, format='XYZ', creationOptions=["ADD_HEADER_LINE=YES"])
        
        # Read the xyz file with pandas

        df  = pd.read_table(xyz_out, skiprows=2, delim_whitespace=True, names=['x', 'y', 'z'])
        
        # Convert the pandas DataFrame to a 2D GeoPandas GeoDataFrame

        gdf2d = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y))

        # Convert the geodataframe to a 2d shapefile
        shp_2d_out = shp_2d + code + "_2d.shp"
        gdf2d.to_file(shp_2d_out)
    
    else: 
        print("BHM-" + code + "_reprojected.tif was not found")



# b) Mask the maxar georeferenced raster tifs using BHM_reprojected_2d.shp point shapefiles 

for code in grid_extent["qmdt_cod"]:
    
    if file_exists(shp_2d + code + "_2d.shp"): 
        shapefile = shp_2d + code + "_2d.shp"
        with fiona.open(shapefile, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
        
        with rasterio.open(output_maxar_data + code + "_georef.tif") as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            out_meta = src.meta
        out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})
        with rasterio.open(cropped_maxar + code + "_cropped.tif", "w", **out_meta) as dest:
            dest.write(out_image)
            
    else: 
        print(code + "_2d.shp was not found")






