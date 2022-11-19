"""
A script to download the relevant data from the Sentinel sattelite, and then resized to be paired.
"""
# package imports
import ee
import numpy as np
import pandas as pd
from pyproj import Transformer
import urllib.request
import sys
import json
from datetime import datetime

# activation of GEE
ee.Authenticate()

# initialize gee
ee.Initialize()


def load_ref_coords(path, filename):
    """Load the csv which contains the reference co-ordinates."""
    df_coords = pd.read_csv(path + filename)

    return df_coords


def save_sentinel_image(df_coords, i, image_parameters):

    # split image parameters into separate variables
    image_collection = image_parameters["image_collection"]
    date_initial = image_parameters["start_date"]
    date_final = image_parameters["end_date"]
    bands = image_parameters["bands"]
    image_bounds = image_parameters["image_bounds"]

    # first retrieve the co-ordinates
    coords, filecode = get_latlon_coords(df_coords, i)

    # strip the relevant info from filename
    sentinel_filename = filecode + "_Sent1_" + bands[0] + ".tif"

    # get the fdb image
    fdb_img = get_fdb_image(image_collection, coords, date_initial, date_final)

    # select the bands and scale
    url = fdb_img.select(bands).getThumbURL({"min": image_bounds[0], "max": image_bounds[1]})
    
    # save the image
    urllib.request.urlretrieve(url, sentinel_filename)

    coord_row = df_coords.loc[[i]]
    size_x = coord_row.pixel_horiz.values[[0]]
    size_y = coord_row.pixel_vert.values[[0]]
    
    img = Image.open(sentinel_filename)
    img_arr = np.array(img)
    resized = cv2.resize(img_arr, (int(size_x), int(size_y)), interpolation = cv2.INTER_NEAREST)
    resized2 = Image.fromarray(resized)
    resized2.save(sentinel_filename)
    
    return

def get_fdb_image(image_collection, coords, date_initial, date_final):
    """Get an fdb image from a set of co-ordinates."""
    aoi = ee.Geometry.Polygon(coords)
    ffa_db = ee.Image(
        ee.ImageCollection(image_collection)
        .filterBounds(aoi)
        .filterDate(ee.Date(date_initial), ee.Date(date_final))
        .first()
        .clip(aoi)
    )

    return ffa_db

def get_latlon_coords(df_coords, i):
    """Returns a set of lat/long co-ordinates from tif file."""

    # choose a given row
    coord_row = df_coords.loc[[i]]

    # retrive the co-ordinates
    x0 = coord_row.left.values[0]
    x1 = coord_row.right.values[0]
    y0 = coord_row.bottom.values[0]
    y1 = coord_row.top.values[[0]]
    coords_3857 = np.array(
        [[x0, y0], [x0, y1], [x1, y1], [x1, y0]], dtype=object)

    # change - to _ in filename to match with maxar data
    filename = coord_row.file_name.values[0][:8]

    # define the transformer
    transformer = Transformer.from_crs(
        "EPSG:3857", "EPSG:4326", always_xy=True)

    # transform to lat lon (epsg:4326)
    coords_x, coords_y = transformer.transform(
        coords_3857[:, 0], coords_3857[:, 1])

    coords_latlon = np.dstack([coords_x, coords_y])[0].tolist()
    # print(coords_latlon)
    # print([x0],[x1],[y1],[y0])
    # print(coords_x)
    # print(coords_y)
    return coords_latlon, filename

def saving(df_path, image_parameters):

    df_coords = load_ref_coords("", df_path)

    # print(df_coords.head())
    # print(df_coords.info())

    # coords_latlon, filename = get_latlon_coords(df_coords, 1)
    # print(coords_latlon, filename)

    df = pd.read_csv(df_path)
    n = df.shape[0]

    for i in range(n):
        save_sentinel_image(df_coords, i, image_parameters)

    with open("parameters.json", "w") as outfile:
        json.dump(image_parameters, outfile)

    now = datetime.now()
    date_time = now.strftime("%d.%m_%H.%M")
    print("date and time:", date_time)


### user defined inputs ###
# This is what the user has to run to download the Sentinel images:
# 1. It is necessary to specify the directory and file name of the csv containing the co-ordinates:
# df_path = "file.csv"
# The file.csv has to contain the co-ordinates as: left, right, top, bottom; and the image size as: pixel_horiz, pixel_vert
#
# 2. Then, these parameters need to be specified (the data included is an example, see the option in the point 4): 
# image_parameters = {"image_collection": "COPERNICUS/S1_GRD",
#                    "start_date": "2020-09-01",
#                    "end_date": "2020-09-30",
#                    "bands": ["VV"],
#                    "image_bounds": [-25, 5]}
#
# 3. And finally the function is called to run the script to download the data: 
# saving(image_parameters=image_parameters, df_path=df_path)
#
# 4. Possible parameters to download from Sentinel 1 or Sentinel 2:
# COPERNICUS/S2_SR; min: 0.0, max: 3000 bands B4, B3, B2
# COPERNICUS/S1_GRD; min: -25, max: 5 bands VV,VH (these bands can only be downloaded separatelly)