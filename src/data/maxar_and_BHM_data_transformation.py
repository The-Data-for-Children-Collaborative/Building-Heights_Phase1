# Input data

maxar = '[0-9]-[0-9].png' # (example file 2222-234.png)
BHM = 'BHM-[0-9]-[0-9].tif' # (example file BHM-2222-234.tif)


## Georeferencing maxar data

from osgeo import gdal
ds = gdal.Translate('maxar_georef.png', maxar, options='-a_srs EPSG:3857 -a_ullr <left> <top> <right> <bottom>') 

## Reproject BHM.tif from EPSG:31983 to EPSG:3857 

from osgeo import gdal

wrap = gdal.Warp('BHM_reprojected.tif', BHM , dstSRS='EPSG:3857')

## Crop the maxar raster using a BHM shapefile 

BHM_repro = 'BHM_reprojected.tif'

maxar_georef = 'maxar_georef.png'

# 1) Convert the raster file BHM_repro.tif to 2D point shapefile .shp (This extracts the geometry information from the BHM_repro.tif file)

# a) Transform the tif to xyz

from osgeo import gdal
outDs = gdal.Translate("BHM_repro.xyz", BHM_repro, format='XYZ', creationOptions=["ADD_HEADER_LINE=YES"])

# b)  Read the xyz file with pandas

import pandas as pd
xyz = "BHM_repro.xyz"
df  = pd.read_table(xyz, skiprows=2, delim_whitespace=True, names=['x', 'y', 'z'])
print(df.head(3))

# c) Convert the pandas DataFrame to a 2D GeoPandas GeoDataFrame

import geopandas as gpd
gdf2d = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y))
print(gdf2d.head(3))

# d) and then to shapefile
gdf2d.to_file("BHM_repro_2d.shp")

# 2) Masking the raster file maxar_georef.png using the BHM_repro_2d.shp shapefile (This crops the maxar_georef.png using the geometry of the BHM_repro.tif file)

# a) Using rasterio with fiona, we open the shapefile, read geometries, 

import fiona
import rasterio
import rasterio.mask

shapefile = "BHM_repro_2d.shp"

with fiona.open(shapefile, "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

# and mask out regions of a raster that are outside the polygons defined in the shapefile.

with rasterio.open(maxar_georef) as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta

# b) Crop the maxar_georef.png to the size of BHM_repro.tif . CAUTION!! This command REPLACES the original maxar_georef.png with a cropped png.

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open(maxar_georef, "w", **out_meta) as dest:
    dest.write(out_image)






