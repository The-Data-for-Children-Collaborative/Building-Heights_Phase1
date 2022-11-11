# IMELE-based training routines

This folder contains routines to train the model, given a series of pairs of satellite images and height reference data.

The network architechture and parts of the code are based on https://github.com/speed8928/IMELE.

Run the training routines with the following command

    python train.py --csv list.csv --prefix /data/trained_models/hires/ --data hires01

after having written in `list.csv` a series of pairs (file containing a satellite image,file containing a height reference).
A snapshot of the model weights will be saved in the specified (`prefix`) directory after each epoch.
An additional command line switch `--test test_dataset.csv` will validate the model after each epoch on a test dataset.

One needs to download a pretrained version of the SENet network for transfer learning, which can be done once and for all with the command

     wget -O pretrained_model/encoder/senet154-c7b49a05.pth --no-check-certificate -c http://data.lip6.fr/cadene/pretrainedmodels/senet154-c7b49a05.pth

The code requires CUDA for working which is not available on most laptops and on Amazon WorkSpaces.
