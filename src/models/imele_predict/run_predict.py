#import libraries
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--epochs')
parser.add_argument('-md', '--modeldir')
parser.add_argument('-m', '--model')
parser.add_argument('-p', '--pairs')
args = parser.parse_args()

# epoch for which want to make predictions 
epochs=(args.epochs)
epochs=epochs.split(',')


# pairs for which want to make predictions, e.g. pairs_17 
pairs=(args.pairs)
pairs=pairs.split(',')

# which model, model trained on pairs 17 = 17only, treined on pairs 16&17 = 16a17
model=str(args.model) 
model_dir=os.path.expanduser(args.modeldir)

for pair in pairs:
    pair=str(pair)
    for epoch in epochs:
            epoch=str(epoch)
            prediction_csv="../../../data/processed/prediction_datasets/prediction_maxar_"+pair+"_model_"+model+"_epoch"+epoch+".csv"
            command="python -u eval.py --csv "+prediction_csv+" --model "+model_dir+"model_"+epoch+".pth.tar | tee log_predict_"+model+"_epoch"+epoch+".txt"
            os.system(command)
