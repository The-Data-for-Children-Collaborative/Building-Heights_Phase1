#### converts BHM images in numpy arrays and it crops them in 500 x 500
# Original images are stored in '2222-BHM' , converted images are stored in 'converted_2222-BHM', sliced images are stored in ''2222-BHM_sliced

import numpy as np
from PIL import Image
from numpy import asarray
import os
import pandas as pd

height = 500  #height of cropped image
width = 500  #weight of cropped image
Rx = 200  # overlap of cropping x-axis
Ry = 200  # overlap of cropping y-axis


# starting directories
directory = '2222-BHM'
new_directory = 'converted_2222-BHM'
sliced_dir = '2222-BHM_sliced'


#check if the directory exists already
if os.path.isdir(new_directory) == False :
    os.makedirs(new_directory)

#check if the directory exists already
if os.path.isdir(sliced_dir) == False :
    os.makedirs(sliced_dir)


# iterate over files in that directory
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

            # transform numpydata in a .npy file called 'converted_file_name'
            # save the file in new_directory
            path_join = os.path.join(new_directory, 'converted_' + file_name + '.npy')
            np.save(path_join , numpydata)


            #charge data from the array
            startx=0
            starty =0
            y,x = numpydata.shape

            print('File :', file_name, ' Size :', numpydata.shape)


            ##counter of cropped images

            counter =0

            #crops the file
            while (starty + height < numpydata.shape[0]):
                print('cropping on y...')
                while (startx+width < numpydata.shape[1]):
                    print('cropping on x...')
                    cropped = numpydata[starty:starty+height, startx:startx+width]

                    # saves the cropped array
                    path_join = os.path.join(sliced_dir, file_name + '_y' + str(starty) + 'x' + str(startx) + '.npy')
                    np.save(path_join , cropped, allow_pickle=True)
                    print('Cropped image name:', path_join , 'Shape: ', cropped.shape)
                    counter += 1

                    # reinitialize startx
                    startx = startx + width - Rx
                    print('Not the last block, keep going...', starty, startx)

                    # JUST ADDED: saves the last block
                    if startx + width >= numpydata.shape[1] -1:
                        startx = numpydata.shape[1] - 1
                        last_block = numpydata[starty: starty + height, startx - width : startx]
                        path_join = os.path.join(sliced_dir, file_name + '_y' + str(starty) + 'x' + str(startx-width) + '.npy')
                        np.save(path_join , last_block, allow_pickle=True)
                        counter +=1
                        print('Last block of the row x: ', path_join , 'Shape: ', last_block.shape, 'Coordinates', starty, startx)


                starty = starty + height - Ry
                startx = 0


                # saves the last block #
                if (starty + height >= numpydata.shape[0] -1) and (numpydata.shape[1] >= 500):
                    print('here')
                    starty = numpydata.shape[0] - 1
                    last_block = numpydata[starty - height: starty, startx : startx + width]
                    path_join = os.path.join(sliced_dir, file_name  + '_y' + str(starty-height) + 'x' + str(startx) + '.npy')
                    np.save(path_join , last_block, allow_pickle=True)
                    counter +=1
                    print('Last block of the column y: ', path_join , 'Shape: ', last_block.shape)
                    break


            print('Coordinates last block ', starty, startx, '\n Number of cropped blocks: ', counter, '\n \n')

        #print('Original shape:', numpydata.shape, 'Cropped shape: ', cropped.shape)

        print('Number of cropped photos from the current image: ', counter, '\n \n')
