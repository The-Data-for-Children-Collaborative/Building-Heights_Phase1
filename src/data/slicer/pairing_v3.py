# prepares a csv with pairs of converted files

import numpy as np
from PIL import Image
from numpy import asarray
import os
import pandas as pd
import sys




#check that number of arguments
#if sys.argc != 5:
#    print('Error! We want 5 args')

maxar = sys.argv[1]
BHM = sys.argv[2]
destination = sys.argv[3]

##### RECORDS THE PAIRINGS OF DATA (unsliced) ####

#folder_1 = 'maxar_tiles'
#folder_2 = '2222-BHM'

## iterate over files in that directory
#for file in os.scandir(folder_1):
#    if file.is_file():

#        # extract file name
#        file_name_ext = os.path.basename(file)
#        print(file_name_ext)
#        #file_name = os.path.splitext(file_name_ext)[0]

list_of_files_maxar = sorted(filter( lambda x: os.path.isfile(os.path.join(maxar, x)),
                        os.listdir(maxar) ) )


list_of_files_BHM = sorted( filter( lambda x: os.path.isfile(os.path.join(BHM, x)),
                        os.listdir(BHM) ) )

df = pd.DataFrame({"FILE MAXAR" : list_of_files_maxar, "FILE BHM" : list_of_files_BHM})
path = destination + '/pairings.csv'
df.to_csv( path , index=False)
print(df)
