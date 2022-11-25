# Description to data and directories on S3

## Directories on S3 (~/data on AWS)

### Prediction, plots and error calculation for final model.
Predictions and error calculations done on TST1 (*UNICEF_data/tim_maxartim_maxar_bhm_final_pairs/pairs_24/train_maxar_sliced*)
with the final/"best" trained model. This model can be found *trained_models/brazil/final_model/model_30_mask_2m.pth.tar*
*maxar_final_model_predictions*  
*maxar_final_model_predictions_plots*  
*error_histograms* 

### Test of aplying super-resolution to maxar to meet Doublin-data (OSI_Dataset) resolution and and make predictions using the weights from the OSI_Dataset.
- *superresolution_result*  
Results from super_resolution (used this approach <https://github.com/S2DSLondon/Autumn22_DFCCU/tree/main/notebooks/superresolution/GFP_GAN.ipynb>)    

- *sliced_super_resolution_valentina*  
images in *superresolution_result* sliced into 500x500 pixel slices and saved as numpy-arrays using this script **????**
test_pretrained_model_superres_maxar  

### Trained model weights on OSI_Dataset (Dublin) and maxar (Brazil). 

Subdirectories correspond to the directories under *UNICEF_data/tim_maxar_bhm_final_pairs* that those models were traied on for *trained_models/brazil*. *trained_models/doublin* correspond to training on *OSI_Dataset*
*trained_models*   
*training_logs*  

### Original data that the imele model (found under <https://github.com/S2DSLondon/Autumn22_DFCCU/tree/main/src/models/>)

- *OSI_Dataset* original data  
- *OSI_test_16112022* predictions on that data  
- *external* traied weights the model came with **????**  
- *imele_data.zip* corresponding zip file **????**

### UNICEF_data: contains most of the data 
subdirectories: 
- original data:   
*'Data for Building Height Modeling in Brazil .docx'*   
*height-model.zip*  
*height-model*  
*kaggle_maxar_tiles.zip*  
*kaggle_maxar_tiles*  
*grids_extent.csv* - co-ordinate extents of the original Maxar files

- final data: See also report, section "Creating our dataset: aligned Maxar-BHM pairs"   
    - *tim_maxar_bhm_final_pairs*   
Subdirectories *pairs_10* and *pairs_17* contain subdirectories with predictions.
        -  *pairs_17/train_maxar_sliced_prediction_** use models found under *trained_models/brazil/pair_17_17_11* or *trained_models/brazil/pairs_16_17_17_11*  
        errors on centroids for selected predictions can be found under *pairs_17/prediction_error*
        - *pairs_10/train_maxar_sliced_predict* contain predictions done with models under *trained_models/brazil/pairs_10* --> these are the failed training as trained on the higly vegetaed tiles in *pairs_10*
        - */pairs_10/train_maxar_sliced_prediction_pairs** contrain predictions with the corresponding (directory and then epoch) models in *trained_models/brazil*  
        for predictions *pairs_10/train_maxar_sliced_prediction_pairs_10_17_veg_mask_epoch1000* and *pairs_10/train_maxar_sliced_prediction_pairs_10_17_veg_mask_epoch2* the number at the end does not correspond to the epoch but the vegetation threshold applied in the training.  
        - all predictions have been performed on validation data sets and done using <https://github.com/S2DSLondon/Autumn22_DFCCU/tree/main/src/models/imele_predict/eval.py> 


- subset of final maxar tif files converted to png to feed into superresolution  
*tim_maxar_bhm_final_pairs_convert_png*   

- *summary_data*: contains csv files with co-ordinate and pixel details for BHM/VHM/maxar images, and lists of files in the `file_lists` sub-directory 
 
- *height-model-copy* - copy of the height model files, required for data pipeline
- *kaggle_maxar_tiles_copy* - copy of the Maxar files, useful for testing
- *height_model_subset* - subset of height model files, useful for testing       
- *kaggle_maxar_tiles_subset* - subset of Maxar files, useful for testing

- **????** can these get deleted? if not please add description!     
data     
Valentina  
UNICEF_data/tim_maxar_bhm_final_pairs/pairs_17/test.py  
UNICEF_data/tim_maxar_bhm_final_pairs/pairs_17/sliced_maxar_v4   

                                    

## **????** What are these? What can be deleted? Or please add description! 

all directories under ~/data:  

maxar_slicer_v2.py    
maxar_pseudo_mercator_edges.csv  
height_model_file_pseudo_mercator_edges.csv  
height_model_file_edges.csv  
