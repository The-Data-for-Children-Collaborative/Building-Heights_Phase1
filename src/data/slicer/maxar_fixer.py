###Crops the bottom left block from a maxar image and saves it in the directory where all other sliced images are
# the user needs to insert the path to the maxar folder and the path of the sliced directory

import numpy as np
from PIL import Image
from numpy import asarray
import os
import pandas as pd
import sys




#check that number of arguments
#if sys.argc != 5:
#    print('Error! We want 5 args')

directory = sys.argv[1]
sliced_dir = sys.argv[2]
Rx = int(sys.argv[3])
Ry = int(sys.argv[4])

height = 500  #height of cropped image
width = 500  #weight of cropped image

for file in os.scandir(directory):
    if file.is_file():

        # extract file name
        file_name_ext = os.path.basename(file)
        file_name = os.path.splitext(file_name_ext)[0]

        # check that the file is really an image
        if file_name_ext.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.bmp', '.gif')) == True:

            # load the image from directory and convert into numpy array
            img = Image.open(file.path)

            # transform PIL image into a NumPy array
            numpydata = asarray(img)
            if (numpydata.shape[0] >= 500) and (numpydata.shape[1]>=500):
                #charge data from the array
                print('File :', file_name, ' Size :', numpydata.shape)

                startx = numpydata.shape[1] - 1
                starty = numpydata.shape[0] - 1

                #removes the broken file
                broken_file = file_name + '_y' + str(starty) + 'x' + str(startx-width) + '.npy'
                broken_path = os.path.join(sliced_dir, broken_file)

                if os.path.exists(broken_path):
                    os.remove(broken_path)


                #Crops the bottom left block and saves it in sliced_dir according to the usual conventions
                last_block = numpydata[starty - height: starty, startx - width : startx, :]
                path_join = os.path.join(sliced_dir, file_name + '_y' + str(starty - height) + 'x' + str(startx-width) + '.npy')
                np.save(path_join , last_block, allow_pickle=True)
                print('This is the last block: ', path_join , 'Shape: ', last_block.shape)


# Check the size of the images
weird_maxar = []
print('Here is your list of sliced files')
for file in os.scandir(sliced_dir):
    if file.is_file():
        file_name_ext = os.path.basename(file)
        numpy_array = np.load(file)
        print(file_name_ext, numpy_array.shape)

        if numpy_array.shape != (500, 500, 4):
            weird_maxar.append(file_name_ext)

weird_maxar.sort()
print('Here is the list of files with a weird dimension ', weird_maxar)
