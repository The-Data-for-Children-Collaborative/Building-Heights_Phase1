# Data extraction and manipulation

This directory contains scripts to extract and manipulate the various data sources. Please note, most of the scripts can only be run through the Amazon workspace
since the data is read and written to the S3 bucket there.

Brief description of each file:
 
* `regrid_maxar.py`: runs the full data manipulation pipeline for the maxar and BHM files: converts BHM tif files to epsg:3857 co-ordinates, geo-references maxar png files, crops maxar png files to BHM co-ordinates, downsamples BHM resolution to match maxar data. Also creates csv files with summary data from the final transformed images, which can be found in `data/processed/BHM_maxar_csv_files`
* `height_model_file_edges.py`: extracts pixel, co-ordinate, and height data (if applicable) from tif files
* `list_files.py`: makes a list of desired BHM or maxar files
* `filter_files.py`: should be run only after `regrid_maxar.py` has generated the final cropped matching pairs and the corresponding csv files. Filters out "small" images (either based on the number of pixels or the average pixel resolution), copies and zips the files into smaller chunks for easier transfer.

To run the main data processing pipleine (from the Amazon workspace): `python regrid_maxar.py`. User-specific information is entered from command-line prompts.
