This directory contains the slicer routines.

* `maxar_slicer_v3.py` iterates over all the maxar files of arbitrary size N x M x 4 in a folder whose path is entered through the command line and does the following :
    1. creates a first new folder with name and path entered by the user through command line
      (recommended name `converted_maxar`);
    2. converts every file `filename.tif` in a numpy array `converted_filename.npy`
    3. saves `converted_filename.npy` in the folder and path entered by the user in 1.
    4. creates a second new folder with name and path entered by the user through the command line
      (recommended name `sliced_maxar`)
    5. goes over the converted numpy array and slice it in pieces 500 x 500 x 4 with overlaps entered by the user
      (recommended overlaps `200` and `200`)
    6. saves each slice in the folder created in 4. as `filename_yHxK.py` where:
         - `filename.tif` was the original file
         - `H` is the y-coordinate of the cutting point
         - `K` is the x-coordinate of the cutting point

Example to call it:
` python maxar_slicer_v3.py ~/BLA/BLABLA/maxar ~/BLA/BLABLA/converted_maxar ~/BLA/BLABLA/sliced_maxar 200 200 `


* `BHM_slicer_v3.py` iterates over all the BHM files of arbitrary size N x M in a folder whose path is entered through the command line and does the following :
    1. creates a first new folder with name and path entered by the user through command line
      (recommended name `converted_BHM`);
    2. converts every file `filename.xx` in a numpy array `converted_filename.npy`
    3. saves `converted_filename.npy` in the folder and path entered by the user in 1.
    4. creates a second new folder with name and path entered by the user through the command line
      (recommended name `sliced_BHM`)
    5. goes over the converted numpy array and slice it in pieces 500 x 500 with overlaps entered by the user
      (recommended overlaps `200` and `200`)
    6. saves each slice in the folder created in 4. as `filename_yHxK.py` where:
         - `filename.xx` was the original file
         - `H` is the y-coordinate of the cutting point
         - `K` is the x-coordinate of the cutting point

Example to call it:
` python BHM_slicer_v3.py ~/BLA/BLABLA/BHM ~/BLA/BLABLA/converted_BHM ~/BLA/BLABLA/sliced_BHM 200 200 `

#IMPORTANT : unless you have a good reason to change the overlaps, always use `200 200` when calling the routines.



* `pairing_v3.py` creates a file `pairing.csv` with sorted pairs of maxar and bhm files and saves in a folder entered by user through the command line. An example of the output is `test_file.csv` contained in this folder.  

  (recommended: chose the folder `BLA/BLABLA` which contains both `maxar` and `BHM` )

Examples about how to call it:

o if you want to pair the slices:
` python pairing_v3.py ~/BLA/BLABLA/sliced_maxar ~/BLA/BLABLA/sliced_BHM ~/BLA/BLABLA/sliced_maxar ~/BLA/BLABLA ``

o if you want to pair the converted figures:

` python pairing_v3.py ~/BLA/BLABLA/converted_maxar ~/BLA/BLABLA/sliced_BHM ~/BLA/BLABLA/converted_maxar ~/BLA/BLABLA ``

o if you want to pair the original figures:

` python pairing_v3.py ~/BLA/BLABLA/maxar ~/BLA/BLABLA/sliced_BHM ~/BLA/BLABLA/maxar ~/BLA/BLABLA `


#IMPORTANT : Always respect the order  `python pairing_v3 MAXAR_PATH  BHM_PATH  FINAL_DESTINATION' 
