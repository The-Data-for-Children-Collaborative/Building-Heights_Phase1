"""
A script to download the relevant data from the Sentinel 2 sattelite.
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

### user defined inputs ###
image_collection = "COPERNICUS/S2_SR"
start_date = "2020-09-01"
end_date = "2020-09-30"
bands = ["B2", "B3", "B4"]
image_bounds = [0, 3000]

image_parameters = {
    "image_collection": "COPERNICUS/S2_SR",
    "start_date": "2020-09-01",
    "end_date": "2020-09-30",
    "bands": ["B2", "B3", "B4"],
    "image_bounds": [0, 3000],
}


# initialize gee
ee.Initialize()


def load_ref_coords(path, filename):
    """Load the csv which contains the reference co-ordinates."""
    df_coords = pd.read_csv(path + filename)

    return df_coords


def save_sentinel_image(df, i, image_parameters):

    # split image parameters into separate variables
    image_collection = image_parameters["image_collection"]
    date_initial = image_parameters["start_date"]
    date_final = image_parameters["end_date"]
    bands = image_parameters["bands"]
    image_bounds = image_parameters["image_bounds"]

    # first retrieve the co-ordinates
    coords, filecode = get_latlon_coords(df, i)

    # strip the relevant info from filename
    sentinel_filename = "stl2_" + str(i) + "_" + filecode + ".png"

    # get the fdb image
    fdb_img = get_fdb_image(image_collection, coords, date_initial, date_final)

    # select the bands and scale
    url = fdb_img.select(bands).getThumbURL(
        {"min": image_bounds[0], "max": image_bounds[1]}
    )

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
    coord_row = df_coords.loc[[i]]

    # retrive the co-ordinates
    x0 = coord_row.left.values[0]
    x1 = coord_row.right.values[0]
    y0 = coord_row.bottom.values[0]
    y1 = coord_row.top.values[[0]]
    coords_3857 = np.array([[x0, y0], [x0, y1], [x1, y1], [x1, y0]], dtype=object)

    # change - to _ in filename to match with maxar data
    filename = coord_row.file_name.values[0][:8]

    # define the transformer
    transformer = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)

    # transform to lat lon (epsg:4326)
    coords_x, coords_y = transformer.transform(coords_3857[:, 0], coords_3857[:, 1])

    coords_latlon = np.dstack([coords_x, coords_y])[0].tolist()
    print(coords_latlon)

    return coords_latlon, filename


if __name__ == "__main__":
    df_coords = load_ref_coords(
        "/home/tim/data/UNICEF_data/summary_data/", "BHM_merged.csv"
    )
    print(df_coords.head())
    print(df_coords.info())

    # coords_latlon, filename = get_latlon_coords(df_coords, 1)
    # print(coords_latlon, filename)

    for i in range(1):
        save_sentinel_image(df_coords, i, image_parameters)

    with open("parameters.json", "w") as outfile:
        json.dump(image_parameters, outfile)

    now = datetime.now()
    date_time = now.strftime("%d.%m_%H.%M")
    print("date and time:", date_time)

    # save_sentinel_image(
    #     df_coords_full,
    #     "full",
    #     image_collection,
    #     start_date,
    #     end_date,
    #     image_bounds,
    #     bands,
    # )
