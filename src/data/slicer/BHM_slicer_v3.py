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
new_directory = sys.argv[2]
sliced_dir = sys.argv[3]
Rx = int(sys.argv[4])
Ry = int(sys.argv[5])

height = 500  #height of cropped image
width = 500  #weight of cropped image


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
            # saves it in new_directory
            path_join = os.path.join(new_directory, 'converted_' + file_name + '.npy')
            np.save(path_join , numpydata)


            #charge data from the array
            #height = 500
            #width = 500
            startx=0
            starty =0
            y,x = numpydata.shape
            #Rx = 200  # correction of cropping  x-axis
            #Ry = 200  # correction of cropping y-axis

            print('File :', file_name, ' Size :', numpydata.shape)


            #counter of cropped images
            counter =0

            #crops the file
            while (starty + height < numpydata.shape[0]):
                print('cropping on y...')

                while (startx+width < numpydata.shape[1]):
                    print('cropping on x...')
                    cropped = numpydata[starty:starty+height, startx:startx+width]

                    #saves the cropped array in sliced_dir

                    path_join = os.path.join(sliced_dir, file_name + '_y' + str(starty) + 'x' + str(startx) + '.npy')
                    np.save(path_join , cropped, allow_pickle=True)
                    print('Cropped image name:', path_join , 'Shape: ', cropped.shape)
                    counter += 1
                    # if it's not the last block, we re-initializes x
                    startx = startx + width - Rx
                    print('Not the last block, keep going...', starty, startx)
                    #print(starty, startx)

                    # saves the last block of the row
                    if startx + width >= numpydata.shape[1] -1:
                        startx = numpydata.shape[1] - 1
                        last_block = numpydata[starty: starty + height, startx - width : startx]
                        path_join = os.path.join(sliced_dir, file_name + '_y' + str(starty) + 'x' + str(startx-width) + '.npy')
                        np.save(path_join , last_block, allow_pickle=True)
                        counter +=1



                starty = starty + height - Ry
                startx = 0

            #when I exit the while loop I am here:
            # startx = 0
            # starty + height >= numpy.datashape[0]  <-- I am at the bottom of my image
            starty = numpydata.shape[0] - 1
            while (startx+width < numpydata.shape[1]) and (numpydata.shape[0] >= height):
                cropped = numpydata[starty - height: starty, startx : startx + width]
                path_join = os.path.join(sliced_dir, file_name + '_y' + str(starty-height) + 'x' + str(startx) + '.npy')
                np.save(path_join , last_block)
                counter +=1

                startx = startx + width - Rx

                # saves the last block of the row
                if startx + width >= numpydata.shape[1] -1:
                    startx = numpydata.shape[1] - 1
                    last_block = numpydata[starty: starty + height, startx - width : startx]
                    path_join = os.path.join(sliced_dir, file_name + '_y' + str(starty) + 'x' + str(startx-width) + '.npy')
                    np.save(path_join , last_block, allow_pickle=True)
                    counter +=1
                    print('Last block of the row x: ', path_join , 'Shape: ', last_block.shape, 'Coordinates', starty, startx)




            print('Number of cropped photos from the current image: ', counter )
