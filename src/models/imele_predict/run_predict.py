#import libraries
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--epochs')
parser.add_argument('-md', '--modeldir')
parser.add_argument('-m', '--model')
args = parser.parse_args()

#path for data
short_path="~/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_17/"
path=os.path.expanduser(short_path)

# epoch for which want to make predictions !TODO: call for epochs when running script?
epochs=(args.epochs)
epochs=epochs.split(',')

# which model, model trained on pairs 17 = 17only, treined on pairs 16&17 = 16a17
model=str(args.model) #TODO call for model name when running script
model_dir=os.path.expanduser(args.modeldir)

for epoch in epochs:
        epoch=str(epoch)
        prediction_csv="../../../data/processed/prediction_datasets/prediction_maxar_train1711_"+model+"_epoch"+epoch+".csv"
        command="python -u eval.py --csv "+prediction_csv+" --model "+model_dir+"model_"+epoch+".pth.tar | tee log_predict_train1711_"+model+"_epoch"+epoch+".txt"
        os.system(command)
