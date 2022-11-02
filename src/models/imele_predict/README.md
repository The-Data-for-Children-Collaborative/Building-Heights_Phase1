# IMELE-based predictor

This folder contains routines to predict the height, given a series of satellite images and the model weights from a previous training of the model.

The approach and large parts of the code are based on https://github.com/speed8928/IMELE, and one can download from there some generic pre-trained network weights (`Block0_skip_model_110.pth.tar`). This file should be placed in the `data/external/` folder. 

Run the predictor with the following command

    python ./eval.py

after having written in `test0.csv` a series of pairs. The second image in the pair is actually ignored.
