import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import pickle

from src.CONFIG import PICKLE_DIR, RADIUS, FILTER

def get_string(col):

    arr = np.asarray(col)
    
    result = np.all(arr == arr[0])
    
    if result:
        return arr[0]

def map_nans(df):

    df.replace('None', np.nan, inplace=True)
    df.replace('np.nan', np.nan, inplace=True)
    df.replace('NaN', np.nan, inplace=True)
    df.replace('', np.nan, inplace=True)

    df.fillna(value=np.nan, inplace = True)

def save_results(posterior, fit, model_name):
    
    file_names = {'posterior' : f"posterior_{model_name}.pickle",
                        'fit' : f"fit_{model_name}.pickle"}

    dir = os.path.join(PICKLE_DIR, f"{RADIUS}", model_name, f"filter={FILTER}")
    os.makedirs(dir, exist_ok=True)

    for object, name in zip([posterior, fit], ["posterior", "fit"]):
            pickle_out = open(os.path.join(dir, file_names[name]),"wb")
            pickle.dump(object, pickle_out)
            pickle_out.close()