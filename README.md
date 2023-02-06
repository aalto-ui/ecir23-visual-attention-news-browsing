# Fragmented Visual Attention in Web Browsing: Weibull Analysis of Item Visit Times (ECIR '23)

*By Aini Putkonen, Aurélien Nioche, Markku Laine, Crista Kuuramo & Antti Oulasvirta*

This repository accompanies the paper "Fragmented Visual Attention in Web Browsing: Weibull Analysis of Item Visit Times", published at ECIR '23. 

# 1. Set up virtual environment

Create virtual environment:

    python3 -m venv .env

Activate virtual environment:

    source .env/bin/activate

Install required packages

    python3 -m pip install -r requirements.txt

Deactivate virtual environment

    deactivate

## 2. Add raw data

Please download the raw data from: 

    [URL]

The folder paths are configured in ```CONFIG.py```. The data is read from ```data/01-fit-data/filter=True``` by default (make sure to add the data file here). 

## 3. Fit the models

Model fitting can be run using the following command:

    python3 -m src.fit

This will also take a couple of minutes. Results of model fitting are saved as a text file to ```data/02-results/fitting_results_separate.csv``` and ```data/02-results/fitting_results_separatecovariate.csv```.

## 5. Examine results

The results can be examined using the notebook ```notebooks/stan-plots```. The produced plots are saved to ```data/02-results```. Figures 3 and 4 from the paper are re-produced here. 

## Some notes

Note that some of the variables in the repository are named differently to the paper. For instance, the shape ```k=alpha``` and the scale ```sigma=lambda``` to convey to the Stan documentation. The covariate for picture ```p=i```, as to not confuse it with an index in the written paper. The Stan code for the model is saved in ```src/models/weibull.py```. 

## Cite

TBD

## Contact

If you have any questions, do not hesitate to contact the corresponding author at ```aini.putkonen@aalto.fi```.