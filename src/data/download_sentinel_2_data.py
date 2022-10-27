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

# authenticate and initialize gee
# ee.Authenticate()
# ee.Initialize()


def load_ref_coords(path, filename):
    """Load the csv which contains the reference co-ordinates."""
    df_coords = pd.read_csv(path + filename)

    return df_coords


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


def select_coords_from_df(df_coords, i):
    """Returns a set of lat/long co-ordinates from i-th line of dataframe."""
    coord_row = df_coords.iloc[[i]]

    # retrive the co-ordinates
    # x0 = np.abs(coord_row.left.values[0])
    # x1 = np.abs(coord_row.right.values[0])
    # y0 = np.abs(coord_row.bottom.values[0])
    # y1 = np.abs(coord_row.top.values[0])

    # change - to _ in filename to match with maxar data
    filename = "_".join(coord_row.qmdt_cod.values[0].split("-"))

    # set up square corners and convert to latlong (for gee)
    # print(x0, y0)
    (x0, y0) = (334397.081, 7393629.949)
    bl = utm.to_latlon(x0, y0, 23, "K")
    print(bl)
    # br = utm.to_latlon(x1, y0, 23, "K")
    # tr = utm.to_latlon(x1, y1, 23, "K")
    # tl = utm.to_latlon(x0, y1, 23, "K")

    # make a list of the lat-long pairs
    coord_list = []
    for coord in [bl, br, tr, tl]:
        coord_list.append(list(coord))

    output_dict = {"filename": filename, "coords": coord_list}

    return output_dict


if __name__ == "__main__":
    df_coords = load_ref_coords(
        "/home/callow46/Autumn22_DFCCU/data/processed/", "grids_extent.csv"
    )
    print(df_coords.head())
    print(df_coords.info())

    coord_0 = select_coords_from_df(df_coords, 0)
    print(coord_0)
