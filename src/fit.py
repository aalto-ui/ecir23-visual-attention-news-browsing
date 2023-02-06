import pandas as pd
import os
import stan
import numpy as np

from src.models.weibull import CustomWeibull
from src.utils.utils import save_results
from src.CONFIG import FORMATTED_DIR, RADIUS, FILTER

def main():

    separate = True
    covariate = True

    """
    Loading data
    """

    print (f"Loading Stan data from JSON file for radius {RADIUS}")

    file = os.path.join(FORMATTED_DIR, f"filter={FILTER}", f"weibull_data_{RADIUS}.csv")
    
    weibull_data = pd.read_csv(file)

    print (f"Data file used: {file}")

    """
    Instantiate model
    """
    model_instance = CustomWeibull()

    y = weibull_data["y"].to_numpy()
    x = weibull_data["x"].to_numpy()
    i = np.array(weibull_data["i"], dtype=np.int8)
    d = np.array(weibull_data["d"], dtype=np.int8)

    """
    Fit separate model
    """
    
    if separate == True:
        stan_code = model_instance.stan_model_separate()
        data = {"y" : y,
                "N" : len(y),
                "K" : len(np.unique(x)),
                "x" : x}

        print (data)

        print (f"Fitting Stan model (separate)...")
        posterior = stan.build(stan_code, data=data, random_seed=123)
        fit = posterior.sample(num_chains=4, num_samples=1000, num_warmup=500, stepsize=0.00001)

        save_results(posterior = posterior, fit = fit, model_name = "separate")

    """
    Fit separate model with covariates
    """
        
    if covariate == True:

        stan_code = model_instance.stan_model_separate_cov()
        data = {"y" : y,
                "N" : len(y),
                "i" : i,
                "d" : d,
                "K" : len(np.unique(x)),
                "x" : x}

        print (data)

        print (f"Fitting Stan model (separate model with covariates)...")
        posterior = stan.build(stan_code, data=data, random_seed=343)
        fit = posterior.sample(num_chains=4, num_samples=1000, num_warmup = 500, stepsize=0.00001)

        save_results(posterior = posterior, fit = fit, model_name = "separate_covariate")



if __name__ == "__main__":
    main()