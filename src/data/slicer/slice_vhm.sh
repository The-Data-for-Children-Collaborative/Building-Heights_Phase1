#!/bin/bash

username=$1
pairs_start=$2
pairs_end=$3

pairs=($(seq $pairs_start $pairs_end))
basepath="/home/"$username"/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_"

for pair in "${pairs[@]}"; do
    echo "Doing pairs for folder number" $pair
    # set up directories
    input_path_vhm=$basepath$pair"/vhm/"
    converted_path_vhm=$basepath$pair"/converted_vhm/"
    sliced_path_vhm=$basepath$pair"/sliced_vhm/"
    #rm -rf $converted_path_vhm $sliced_path_vhm
    # slice the VHM files
    #python BHM_slicer_v3.py $input_path_vhm $converted_path_vhm $sliced_path_vhm 200 200
    # apply the fixer
    #python BHM_fixer.py $input_path_vhm $sliced_path_vhm 200 200
    # run the train test split
    python ../train_test_split.py $pair
done



