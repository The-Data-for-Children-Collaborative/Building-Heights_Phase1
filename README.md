# DFCCU: Predicting building height from satellite images

The aim of this project is to use a convolutional-deconvolutional neural network (such as the one described [here](https://arxiv.org/abs/1802.10249) or [here](https://www.mdpi.com/2072-4292/12/17/2719)) to predict building height data from satellite images. 

The building height data covers a region of Sao Paulo and can be downloaded from [this repository](https://www.kaggle.com/datasets/andasampa/height-model).

We will (eventually) use three sources of satellite images: high-resolution maxar data (not publicly available), lower resolution data from [Sentinel 2](https://developers.google.com/earth-engine/datasets/catalog/sentinel-2), and radar images from [Sentinel 1](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD).

Currently, this model [here](https://github.com/speed8928/IMELE) is being used, see src/model/imele_predict for a functioning code for predicting height with preset weights.

The pipeline for data preprocessing (georeferecing, downscaling building height data, cropping images to same size) can be found in src/data.

### Installation
------------

The packages required to run the CNN model can be obtained via

    pip install -r requirements.txt
    
For the data processing gdal and for inspecting the building height model rioxarray are required, which can be installed via conda.  
All packages needed for data processing and error calculation are listed in requirements_data.txt.  

For obtaining the Sentinel data the package earthengine-api is needed as well as a account for the earth-engine. Please follow the instructions given here <https://developers.google.com/earth-engine/guides/python_install>

For running the superresolution, please follow instructions in the corresponding notebook.

### Sentinel specific instructions
------------

1. Set up a conda environment using the `envs/sentinel.yml` file as follows:
`conda env create -f sentinel.yml`
2. Activate the environment with `conda activate sentinel`
3. Register for a google earth engine account [here](https://signup.earthengine.google.com/#!/)
4. Install `gcloud` following the instructions [here](https://cloud.google.com/sdk/docs/install)
5. Authenticate earth engine with the command `earthengine authenticate`. NOTE: If using a cluster / remote machine, this should be done with the `--quiet` flag, i.e. `earthengine authenticate --quiet`.
6. Check it's working by running a Python interpreter with the commands `import ee` and then `ee.Initialize()`. If no errors are thrown then set-up is complete.

### General outline
------------
This project is based on the [Cookiecutter template](http://drivendata.github.io/cookiecutter-data-science/) for data science projects and is structured as follows:

```
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── src                <- Source code for use in this project.
    ├── data           <- Scripts to download or generate data
    │   └── make_dataset.py
    │
    ├── features       <- Scripts to turn raw data into features for modeling
    │   └── build_features.py
    │
    ├── models         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── predict_model.py
    │   └── train_model.py
    │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations
        └── visualize.py

```




