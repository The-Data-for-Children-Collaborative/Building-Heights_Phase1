""" 
script to create csv file and predictiom directory to run predictions
set epochs in line 13 for which want to run predictions
set input data file in line 27 and output data dir in line 19
"""

#import libraries
import pandas as pd
import os

#path for data
short_path="~/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_17/"
path=os.path.expanduser(short_path)

# epoch for which want to make predictions !TODO: call for epochs when running script?
epochs=[6,20,40]

# which model, model trained on pairs 17 = 17only, treined on pairs 16&17 = 16a17
model="pair16_17" #TODO call for model name when running script

for epoch in epochs:
    epoch=str(epoch)

    #path for predictions !TODO: call for dir name when running script
    prediction_dir=path+"train_maxar_sliced_prediction_"+model+"_epoch"+epoch
    if os.path.isdir(prediction_dir)==False:
        command="mkdir "+prediction_dir
        os.system(command)
    else:
        print("WARNING! \n"+prediction_dir+" already exists.\n Check content before making predictions saved to this directory!")

#load input data and ground truth that are for validation, not trained on 
#!TODO call for file when running script, or adapt script to run predictions on all input files in a dir
short_csv="../../../data/processed/validation_filelists/val_list_17.csv"
df_predict_data=pd.read_csv(short_csv,
                           names=["data","ground_truth"],header=None)
df_predict_data["prediction"]=df_predict_data.data


#set dir to correspond in ~/data in dataframe
for index, row in df_predict_data.iterrows():
    row.data=path+"train_maxar_sliced/"+os.path.basename(os.path.realpath(row.data))
    row.ground_truth=path+"train_maxar_sliced/"+os.path.basename(os.path.realpath(row.ground_truth))

for epoch in epochs:
    epoch=str(epoch)
    prediction_dir=path+"train_maxar_sliced_prediction_"+model+"_epoch"+epoch
    for index, row in df_predict_data.iterrows():
        row.prediction=prediction_dir+"/"+os.path.basename(os.path.realpath(row.data))

#save csv file used for eval.py for predictiona
    prediction_csv="../../../data/processed/prediction_datasets/prediction_maxar_train1711_"+model+"_epoch"+epoch+".csv"
    if os.path.isfile(prediction_csv)==False:
        df_predict_data[["data","prediction"]].to_csv(prediction_csv,
                                                index=False,
                                                header=False)
        print(prediction_csv+" created")
    else:
        print("Warning!"+prediction_csv+"already exists! \n Check "+prediction_dir+"for already excisting predictions!")
