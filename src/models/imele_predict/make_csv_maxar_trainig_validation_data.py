""" 
script to create csv file and predictiom directory to run predictions
set epochs in line 13 for which want to run predictions
set input data file in line 27 and output data dir in line 19
"""

#import libraries
import pandas as pd
import os
import glob


"""Return True / False based on y/n input."""
def _tf_from_yn(yn):
    if yn == "y":
        return True
    else:
        return False

#path for data
pairs=input("Please enter pairs to predict on (e.g. pairs_17)")
short_path="~/data/UNICEF_data/tim_maxar_bhm_final_pairs/"+pairs+"/"
path=os.path.expanduser(short_path)
datadir=path + "train_maxar_sliced"
use_default_datadir = _tf_from_yn(
                input("Use default data directory (" + datadir + ")? [y/n] ")
                    )
if not use_default_datadir:
    datadir=input("Please enter data directory: ")

# epoch for which want to make predictions !TODO: call for epochs when running script?
epochs=input("Please enter epochs seperated by ',': ")
epochs=epochs.split(',')

# which model, model trained on pairs 17 = 17only, treined on pairs 16&17 = 16a17
model=input("Please enter model name,e.g. over which  pairs the model was trained: ") 

#set path to save predictions in
predictiondir=path+"train_maxar_sliced_prediction_"+model+"_epoch"
use_default_predictiondir = _tf_from_yn(
                        input("Use default prediction directory (" + predictiondir + "??, with ?? replced by epoch number) ? [y/n] ")
                                            )
if not use_default_predictiondir:
    predictiondir=input("Please enter prediction directory (epoch number will be added at the end): ")

for epoch in epochs:
    epoch=str(epoch)

    prediction_dir=predictiondir+epoch
    if os.path.isdir(prediction_dir)==False:
        command="mkdir "+prediction_dir
        os.system(command)
        print(prediction_dir + "created")
    else:
        print("WARNING! \n"+prediction_dir+" already exists.\n Check content before making predictions saved to this directory!")
        abort= input("Do you want to continue?  [y/n] ") 
        if abort=="n":
            exit()

#load input data and ground truth that are for validation, not trained on 
use_all_files = _tf_from_yn(
                            input("Use all files in " + datadir + "? [y/n] ")
                                                                            )
list_files=[]
for name in glob.glob(datadir+"/*npy"):
    list_files.append(name)
df_data_predict=pd.DataFrame({'data':list_files,'prediction':list_files})

if not use_all_files:
                            csv_prediction_files=input("Please enter directory with csv listing files for prediction (in first column). ")
                            short_csv="../../../data/processed/validation_filelists/val_list_17.csv"
                            if csv_prediction_files==short_csv:
                                df_data_predict=pd.read_csv(short_csv,
                                                            names=["data","ground_truth"],header=None)
                                df_data_predict["prediction"]=df_data_predict.data


                                #set dir to correspond in ~/data in dataframe
                                for index, row in df_data_predict.iterrows():
                                    row.data=path+"train_maxar_sliced/"+os.path.basename(os.path.realpath(row.data))
                                    row.ground_truth=path+"train_maxar_sliced/"+os.path.basename(os.path.realpath(row.ground_truth))

                                for epoch in epochs:
                                    epoch=str(epoch)
                                    prediction_dir=path+"train_maxar_sliced_prediction_"+model+"_epoch"+epoch
                                    for index, row in df_data_predict.iterrows():
                                        row.prediction=prediction_dir+"/"+os.path.basename(os.path.realpath(row.data))

                                #save csv file used for eval.py for predictiona
                                    prediction_csv="../../../data/processed/prediction_datasets/prediction_maxar_train1711_"+model+"_epoch"+epoch+".csv"
                                    if os.path.isfile(prediction_csv)==False:
                                        df_data_predict[["data","prediction"]].to_csv(prediction_csv,
                                                                                index=False,
                                                                                header=False)
                                        print(prediction_csv+" created")
                                    else:
                                        print("Warning!"+prediction_csv+"already exists! \n Check "+prediction_dir+"for already excisting predictions!")
                            
                            else:
                                df_data_predict=pd.read_csv(csv_prediction_files, usecols = [0], names=["data"], header=None)
                                df_data_predict["prediction"]=df_data_predict.data


#set dir to correspond in ~/data in dataframe
for index, row in df_data_predict.iterrows():
    row.data=datadir+"/"+os.path.basename(os.path.realpath(row.data))

for epoch in epochs:
    epoch=str(epoch)
    prediction_dir=predictiondir+epoch
    for index, row in df_data_predict.iterrows():
        row.prediction=prediction_dir+"/"+os.path.basename(os.path.realpath(row.data))

#save csv file used for eval.py for predictiona
    prediction_csv="../../../data/processed/prediction_datasets/prediction_maxar_"+pairs+"_model_"+model+"_epoch"+epoch+".csv"
    if os.path.isfile(prediction_csv)==False:
        df_data_predict[["data","prediction"]].to_csv(prediction_csv,index=False, header=False)
        print(prediction_csv+" created")
    else:
        print("Warning!"+prediction_csv+"already exists! \n Check "+prediction_dir+"for already excisting predictions!")
