# IMELE-based training routines

This folder contains routines to train the model, given a series of pairs of satellite images and height reference data.

The approach and large parts of the code are based on https://github.com/speed8928/IMELE.

Run the training routines with the following command

    python train.py --csv list.csv

after having written in `list.csv` a series of pairs (file containing a satellite image,file containing a height reference). 

One needs to download a pretrained version of the SENet network for transfer learning, which can be done once and for all with the command

     wget -O pretrained_model/encoder/senet154-c7b49a05.pth --no-check-certificate -c http://data.lip6.fr/cadene/pretrainedmodels/senet154-c7b49a05.pth

This is still a work in progress, the code requires CUDA for working which is not available on most laptops and on Amazon WorkSpaces.
