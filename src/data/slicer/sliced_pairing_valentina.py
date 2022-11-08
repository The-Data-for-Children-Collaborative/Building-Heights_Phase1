# prepares a csv with the path of pairs of sliced files

import numpy as np
from PIL import Image
from numpy import asarray
import os
import pandas as pd


#starting folders
folder_1 = 'maxar_sliced'
folder_2 = '2222-BHM_sliced'

#sorts the files in folder_1
list_1 = sorted( filter(lambda x: os.path.isfile(os.path.join(folder_1, x)),
                        os.listdir(folder_1) ))

#print(len(os.listdir(folder_1)))

#adds the prefix with the path to every element of the list
prefix_1 = './' + folder_1 + '/'
list_1 = [prefix_1 + x for x in list_1]

#print(list_1)

#sorts the files in folder 2
list_2 = sorted( filter( lambda x: os.path.isfile(os.path.join(folder_2, x)),
                        os.listdir(folder_2) ) )

#print(len(os.listdir(folder_2)))

#adds the prefix with the path to every element of the list
prefix_2 = './' + folder_2 + '/'
list_2 = [prefix_2 + x for x in list_2]

#produces the joint dataframe
df = pd.DataFrame({ ' SLICED MAXAR' : list_1, ' SLICED BHM' : list_2})
df.to_csv("test_file_sliced.csv", index=False)
print(df)
