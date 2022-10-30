"""
A script to download the relevant data from the Sentinel 2 sattelite.
"""

# package imports
import ee
import numpy as np
import pandas as pd
from pyproj import Transformer
import urllib.request


### user defined inputs ###
image_collection = "COPERNICUS/S2_SR"
start_date = "2020-08-01"
end_date = "2020-08-31"
bands = ["B2", "B3", "B4"]
image_bounds = [0, 3000]


# authenticate and initialize gee
ee.Authenticate()
ee.Initialize()


def load_ref_coords(path, filename):
    """Load the csv which contains the reference co-ordinates."""
    df_coords = pd.read_csv(path + filename)

    return df_coords


def save_sentinel_image(
    df, i, image_collection, date_initial, date_final, image_bounds, bands
):

    # first retrieve the co-ordinates
    coords, filecode = get_latlon_coords(df, i)

    # strip the relevant info from filename
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
    coord_row = df_coords.iloc[[i]]

    # retrive the co-ordinates
    x0 = coord_row.left.values[i]
    x1 = coord_row.right.values[i]
    y0 = coord_row.bottom.values[i]
    y1 = coord_row.top.values[i]
    coords_3857 = np.array([[x0, y0], [x0, y1], [x1, y1], [x1, y0]])

    # change - to _ in filename to match with maxar data
    filename = "_".join(coord_row.qmdt_cod.values[0].split("-"))

    # define the transformer
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    # transform to lat lon (epsg:4326)
    coords_x, coords_y = transformer.transform(coords_3857[:, 0], coords_3857[:, 1])
    coords_latlon = np.dstack([coords_x, coords_y])[0].tolist()

    return coords_latlon, filename


if __name__ == "__main__":
    df_coords = load_ref_coords("/home/tim/data/UNICEF_data/", "grids_extent.csv")
    print(df_coords.head())
    print(df_coords.info())

    coords_latlon, filename = get_latlon_coords(df_coords, 0)
    print(coords_latlon, filename)

    save_sentinel_image(
        df_coords, 0, image_collection, start_date, end_date, image_bounds, bands
    )
