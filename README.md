# Pivigo Data Science Template

_A recommended minimal project structure for doing and sharing data science work._


This template is based on the good work from the [Cookiecutter project](http://drivendata.github.io/cookiecutter-data-science/). Please visit the website for a more detailed explanation of how to get the most out of the template and best practices in general. In particular, we strongly suggest that you work in the context of a virtual environment for this project. Please feel free to change the directory structure as you wish. 

The structure we have given you is a lightweight version of the full cookiecutter-data-science template. The full version includes a number of functionalities that are often not needed, such as a Makefile and setup scripts, as well as a .env file for holding keys. In some cases you may want this added functionality and may, therefore, substitute this template for the original cookiecutter-data-science template.


The directory structure of your new project looks like this: 

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

## Contributing

The creators of the Cookiecutter project welcome contributions! [See the docs for guidelines](https://drivendata.github.io/cookiecutter-data-science/#contributing).

### Installing development requirements
------------

    pip install -r requirements.txt

