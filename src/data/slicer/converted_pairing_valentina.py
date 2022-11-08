# prepares a csv with pairs of converted files

import numpy as np
from PIL import Image
from numpy import asarray
import os
import pandas as pd

##### RECORDS THE PAIRINGS OF DATA (unsliced) ####

folder_1 = 'maxar_tiles'
folder_2 = '2222-BHM'

## iterate over files in that directory
#for file in os.scandir(folder_1):
#    if file.is_file():

#        # extract file name
#        file_name_ext = os.path.basename(file)
#        print(file_name_ext)
#        #file_name = os.path.splitext(file_name_ext)[0]

list_of_files_1 = sorted(filter( lambda x: os.path.isfile(os.path.join(folder_1, x)),
                        os.listdir(folder_1) ) )

list_of_files_2 = sorted( filter( lambda x: os.path.isfile(os.path.join(folder_2, x)),
                        os.listdir(folder_2) ) )

df = pd.DataFrame({"FILE MAXAR" : list_of_files_1, "FILE BHM" : list_of_files_2})
df.to_csv("test_file.csv", index=False)
print(df)
