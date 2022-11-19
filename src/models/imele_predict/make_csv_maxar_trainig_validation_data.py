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
epochs=[12, 20, 30, 50, 70, 99]

for epoch in epochs:
    epoch=str(epoch)

    #path for predictions !TODO: call for dir name when running script
    if os.path.isdir(path+"train_maxar_sliced_prediction_17only_epoch"+epoch)==False:
        command="mkdir "+path+"train_maxar_sliced_prediction_17only_epoch"+epoch
        os.system(command)
    else:
        print("WARNING! \n"+path+"train_maxar_sliced_prediction_17only_epoch"+epoch+" already exists.\n Check content before making predictions saved to this directory!")

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
    row.prediction=path+"train_maxar_sliced_prediction_17only_epoch"+epoch+"/"+os.path.basename(os.path.realpath(row.data))

for epoch in epochs:
    epoch=str(epoch)
    for index, row in df_predict_data.iterrows():
        row.prediction=path+"train_maxar_sliced_prediction_17only_epoch"+epoch+"/"+os.path.basename(os.path.realpath(row.data))

#save csv file used for eval.py for predictiona
    prediction_csv="../../../data/processed/prediction_datasets/prediction_maxar_train1711_pair17_epoch"
    if os.path.isfile(prediction_csv)==False:
        df_predict_data[["data","prediction"]].to_csv(prediction_csv+epoch+".csv",
                                                index=False,
                                                header=False)
    else:
        print("Warning!"+prediction_csv+"already exists! \n Check"+path+"train_maxar_sliced_prediction_17only_epoch"+epoch+"for already excisting predictions!")
