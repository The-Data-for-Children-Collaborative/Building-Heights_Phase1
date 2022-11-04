# DFCCU: Predicting building height from satellite images

The aim of this project is to train a convolutional-deconvolutional neural network (such as the one described [here](https://arxiv.org/abs/1802.10249) or [here](https://www.mdpi.com/2072-4292/12/17/2719)) to predict building height data from satellite images. 

The building height data covers a region of Sao Paulo and can be downloaded from [this repository](https://www.kaggle.com/datasets/andasampa/height-model).

We will (eventually) use three sources of satellite images: high-resolution maxar data (not publicly available), lower resolution data from [Sentinel 2](https://developers.google.com/earth-engine/datasets/catalog/sentinel-2), and radar images from [Sentiel 1](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD).

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


### Installation
------------

Recommended installation procedure is still to come! For now, the packages required to run the CNN model can be obtained via

    pip install -r requirements.txt

