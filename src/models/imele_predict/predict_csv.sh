#script to create csv file for prediction for specific files in a directory
#input: input file incl. direcotry and directory for putput file (here: train_maxar_sliced_predict)
#uncomment line that want to use for creating csv file
#~/data/UNICEF_data/tim_maxar_bhm_final_pairs/ : dir of maxar input files
#~/data/OSI_Dataset/ : directory of original files for Dubplin that imele was orginally developped on

#for i in ~/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_10/train_maxar_sliced/maxar-3215-113_*.npy ; do echo $i,$(echo $i | sed "s/train_maxar_sliced/train_maxar_sliced_predict/g" ); done > predict_maxar_trained.csv
#for i in ~/data/UNICEF_data/tim_maxar_bhm_final_pairs/pairs_10/train_maxar_sliced/maxar-3215-243*.npy ; do echo $i,$(echo $i | sed "s/train_maxar_sliced/train_maxar_sliced_predict/g" ); done > predict_maxar_trained.csv
#for i in ~/data/OSI_Dataset/train_rgbs_base/315000_234000_RGB_5_1* ; do echo $i,$(echo $i | sed "s/train_rgbs_base/rgbs_predict/g" ); done > predict_OSI_dataset_trained.csv
#for i in ~/data/OSI_Dataset/test_rgbs_base/315000_233500_RGB_10_4* ; do echo $i,$(echo $i | sed "s/test_rgbs_base/rgbs_predict/g" ); done > predict_OSI_dataset_trained.csv
#for i in ~/data/OSI_Dataset/test_rgbs_base/315500_234000_RGB_9_1* ; do echo $i,$(echo $i | sed "s/test_rgbs_base/rgbs_predict/g" ); done > predict_OSI_dataset_trained.csv
