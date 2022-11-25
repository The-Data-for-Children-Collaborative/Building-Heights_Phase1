# Data extraction and manipulation

This directory contains scripts to extract and manipulate the various data sources. Please note, most of the scripts can only be run through the Amazon workspace
since the data is read and written to the S3 bucket there.

Brief description of each file:
 
* `regrid_maxar.py`: runs the full data manipulation pipeline for the maxar and BHM files: converts BHM tif files to epsg:3857 co-ordinates, geo-references maxar png files, crops maxar png files to BHM co-ordinates, downsamples BHM resolution to match maxar data 
* `height_model_file_edges.py`: extracts pixel, co-ordinate, and height data (if applicable) from tif files
* `list_fBHM_files.py`: makes a list of desired BHM files
* `list_maxar_tifs.py`: makes a list of desired maxar files
* `rawToInput.py`: alternative approach to go from raw to input data, it results in more misaligned maxar-BHM pairs than  
regrid_maxar.py 

To run the pipleine (from the Amazon workspace): `python regrid_maxar.py`. Select parts of the pipeline can be run by editing the user input code block in the file.
