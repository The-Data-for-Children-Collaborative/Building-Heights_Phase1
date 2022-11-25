# Data extraction and manipulation

This directory contains scripts to extract and manipulate the various data sources. Please note, most of the scripts can only be run through the Amazon workspace
since the data is read and written to the S3 bucket there.

Brief description of each file:
 
* `regrid_maxar.py`: runs the full data manipulation pipeline for the maxar and BHM files: converts BHM tif files to epsg:3857 co-ordinates, geo-references maxar png files, crops maxar png files to BHM co-ordinates, downsamples BHM resolution to match maxar data. Also creates csv files with summary data from the final transformed images, examples of which can be found in `data/processed/BHM_maxar_csv_files`
* `regrid_vhm.py`: regrids the VHM files to the same extents as the final cropped maxar and BHM files, and writes summary csv files
* `height_model_file_edges.py`: extracts pixel, co-ordinate, and height data (if applicable) from tif files
* `rawToInput.py`: alternative approach to go from raw to input data, it results in more misaligned maxar-BHM pairs than regrid_maxar.py 
* `list_files.py`: makes a list of desired BHM or maxar files
* `filter_files.py`: should be run only after `regrid_maxar.py` has generated the final cropped matching pairs and the corresponding csv files. Filters out "small" images (either based on the number of pixels or the average pixel resolution), copies and zips the files into smaller chunks for easier transfer.
* `train_test_split.py` : splits maxar, bhm and vhm files randomly into train and test folders. Accepts a command line argument for the pairs to split, so should be run for example as `python train_test_split.py 0` for `pairs_0`.
* `download_sentinel.py` : downloads Sentinel-1 and 2 images, for image extents given by a csv file containing a summary of the maxar / BHM co-ordinates and pixel sizes. To run this as a stand-alone script, the comment block at the end of the file needs to be uncommented and modified to the user's wishes.

To run the main data processing pipleine (from the Amazon workspace): `python regrid_maxar.py`. User-specific information is entered from command-line prompts.
