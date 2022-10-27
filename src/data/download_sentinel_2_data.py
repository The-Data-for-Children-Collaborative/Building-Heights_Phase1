"""
A script to download the relevant data from the Sentinel 2 sattelite.
"""

# package imports
import ee
import matplotlib.pyplot as plt
import numpy as np
import IPython.display as disp
import pandas as pd
import utm
import rioxarray
import urllib.request


### user defined inputs ###
image_collection = "COPERNICUS/S2_SR"
start_date = "2020-08-01"
end_date = "2020-08-31"
bands = ["B2", "B3", "B4"]
image_bounds = [0, 3000]


# authenticate and initialize gee
# ee.Authenticate()
ee.Initialize()


def load_ref_coords(path, filename):
    """Load the csv which contains the reference co-ordinates."""
    df_coords = pd.read_csv(path + filename)

    return df_coords


def save_sentinel_image(
    filename, image_collection, date_initial, date_final, image_bounds, bands
):

    # first retrieve the co-ordinates
    coords = get_coords_from_tif(filename)

    # strip the relevant info from filename
    filecode = filename[-12:-4]
    sentinel_filename = "stl2_" + filecode + "_.png"

    # get the fdb image
    fdb_img = get_fdb_image(image_collection, coords, date_initial, date_final)

    # select the bands and scale
    url = fdb_img.select(bands).getThumbURL({"min": 0, "max": 3000})

    # save the image
    urllib.request.urlretrieve(url, sentinel_filename)

    return


def get_fdb_image(image_collection, coords, date_initial, date_final):
    """Get an fdb image from a set of co-ordinates."""
    aoi = ee.Geometry.Polygon(coords)
    print(aoi)
    ffa_db = ee.Image(
        ee.ImageCollection(image_collection)
        .filterBounds(aoi)
        .filterDate(ee.Date(date_initial), ee.Date(date_final))
        .first()
        .clip(aoi)
    )

    return ffa_db


def get_coords_from_tif(filename):
    """Returns a set of lat/long co-ordinates from tif file."""

    # load in the array
    array = rioxarray.open_rasterio(filename, masked=True).squeeze()

    # get the bounding co-ordinates
    x0 = float(array.x[0])
    y0 = float(array.y[0])
    x1 = float(array.x[-1])
    y1 = float(array.y[-1])

    # set up the corners of the image square
    bl = utm.to_latlon(x0, y0, 23, "K")
    br = utm.to_latlon(x1, y0, 23, "K")
    tr = utm.to_latlon(x1, y1, 23, "K")
    tl = utm.to_latlon(x0, y1, 23, "K")

    print(bl, br, tr, tl)

    # make a list of the lat-long pairs
    coord_list = []
    for coord in [bl, br, tr, tl]:
        coord_list.append(list(coord)[::-1])
    return coord_list


if __name__ == "__main__":
    # df_coords = load_ref_coords(
    #     "/home/callow46/Autumn22_DFCCU/data/processed/", "grids_extent.csv"
    # )
    # print(df_coords.head())
    # print(df_coords.info())

    coord_0 = get_coords_from_tif(
        "/home/callow46/Autumn22_DFCCU/data/raw/test_data/BHM-2222-224.tif"
    )

    filename = "/home/callow46/Autumn22_DFCCU/data/raw/test_data/BHM-2222-224.tif"

    save_sentinel_image(
        filename, image_collection, start_date, end_date, image_bounds, bands
    )
