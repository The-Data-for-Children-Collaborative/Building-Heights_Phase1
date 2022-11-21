### Fixes the bug caused by slicer_v3: Crops the bottom left block from a maxar image and saves it in the directory where all other sliced images are
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

destination = sys.argv[1]

#directory_maxar = sys.argv[1]
#sliced_dir_maxar = sys.argv[2]
#directory_bhm = sys.arg[3]
#sliced_dir_bhm = sys.arg[4]

Rx = int(sys.argv[2])
Ry = int(sys.argv[3])


directory_maxar = destination + '/maxar'
directory_bhm = destination + '/bhm'
sliced_dir_maxar = destination + '/sliced_maxar'
sliced_dir_bhm = destination + '/sliced_bhm'

height = 500  #height of cropped image
width = 500  #weight of cropped image

for file in os.scandir(directory_maxar):
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
                broken_path = os.path.join(sliced_dir_maxar, broken_file)

                if os.path.exists(broken_path):
                    os.remove(broken_path)


                #Crops the bottom left block and saves it in sliced_dir according to the usual conventions
                last_block = numpydata[starty - height: starty, startx - width : startx, :]
                path_join = os.path.join(sliced_dir_maxar, file_name + '_y' + str(starty - height) + 'x' + str(startx-width) + '.npy')
                np.save(path_join , last_block, allow_pickle=True)
                print('This is the last block: ', path_join , 'Shape: ', last_block.shape)


for file in os.scandir(directory_bhm):
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

                #initializes startx and starty
                startx = numpydata.shape[1] - 1
                starty = numpydata.shape[0] - 1

                #removes the broken file
                broken_file = file_name + '_y' + str(starty) + 'x' + str(startx-width) + '.npy'
                broken_path = os.path.join(sliced_dir_bhm, broken_file)

                if os.path.exists(broken_path):
                    os.remove(broken_path)


                #Crops the bottom left block and saves it in sliced_dir according to the usual conventions
                last_block = numpydata[starty - height: starty, startx - width : startx]



                path_join = os.path.join(sliced_dir_bhm, file_name + '_y' + str(starty - height) + 'x' + str(startx-width) + '.npy')
                np.save(path_join , last_block, allow_pickle=True)
                print('This is the last block: ', path_join , 'Shape: ', last_block.shape)


# Check the size of the images in maxar
weird_maxar = []
print('Here is your list of sliced files')
for file in os.scandir(sliced_dir_maxar):
    if file.is_file():
        file_name_ext = os.path.basename(file)
        if file_name_ext.endswith(".npy"):
            numpy_array = np.load(file, allow_pickle=True)
            print(file_name_ext, numpy_array.shape)

            if numpy_array.shape != (500, 500, 4):
                weird_maxar.append(file_name_ext)

weird_maxar.sort()
print('Here is the list of files with a weird dimension ', weird_maxar)


#Check the size of the images in bhm
weird_bhm = []
count = 0
print('Here is your list of sliced files')
for file in os.scandir(sliced_dir_bhm):
    if file.is_file():
        file_name_ext = os.path.basename(file)
        if file_name_ext.endswith(".npy"):
            numpy_array = np.load(file, allow_pickle=True)
            print(file_name_ext, numpy_array.shape)
            count +=1
            if numpy_array.shape != (500, 500):
                weird_bhm.append(file_name_ext)

weird_bhm.sort()
print('There are ', count, ' files ')
print('Here is the list of files with a weird dimension ', weird_bhm )


#### fixes the csv file
list_of_files_maxar = sorted(filter( lambda x: os.path.isfile(os.path.join(sliced_dir_maxar, x)),
                        os.listdir(sliced_dir_maxar) ) )


list_of_files_BHM = sorted( filter( lambda x: os.path.isfile(os.path.join(sliced_dir_bhm, x)),
                        os.listdir(sliced_dir_bhm) ) )

if len(list_of_files_maxar) != len(list_of_files_BHM):
    print("Error: the lists have different lengths, " , len(list_of_files_maxar), len(list_of_files_BHM))

else:
    #destination = os.path.commonprefix([sliced_dir_maxar, sliced_dir_bhm]) #common ancestor of the sliced_directory
    df = pd.DataFrame({"FILE MAXAR" : list_of_files_maxar, "FILE BHM" : list_of_files_BHM})
    path = destination + '/pairings.csv'
    df.to_csv( path , index=False)
    print(df)
