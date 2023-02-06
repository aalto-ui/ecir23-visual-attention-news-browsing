class CustomWeibull:

    stan_params = ("alpha", "sigma",)
    param_colors = ("green", "black")
    NAME = "Weibull"

    def __init__(self):
        self.name = "weibull"

    def stan_model_separate(self):
        
            stan_code = """
                    data {
                    int<lower=0> N; // number of observations
                    int<lower=0> K; // number of groups (conditions)
                    int<lower=1,upper=K> x[N]; // indicators for groups (conditions)
                    vector[N] y;    // observations (aggregated)
                    }
                    parameters {
                    real<lower=0> alpha[K];        // pooled alpha (shape) 
                    real<lower=0> sigma[K];        // pooled sigma (scale) 
                    }
                    model {
                        for (k in 1:K){
                            alpha[k] ~ normal(0, 10);  // prior for mu
                            sigma[k] ~ normal(0, 10);   // prior for sigma
                        }
                        for (n in 1:N)
                            y[n] ~ weibull(alpha[x[n]], sigma[x[n]]);  // likelihood / observation model
                    }
                    generated quantities {
                        vector[N] log_lik;
                        vector[N] y_rep;   
                        int<lower = 0, upper = 1> mean_gt;
                        int<lower = 0, upper = 1> sd_gt;
                        for (n in 1:N){
                            log_lik[n] = weibull_lpdf(y[n] | alpha[x[n]], sigma[x[n]]); 
                            y_rep[n] = weibull_rng(alpha[x[n]], sigma[x[n]]);
                            }
                        mean_gt = mean(y_rep) > mean(y);
                        sd_gt = sd(y_rep) > sd(y);
                    }
                    """
            
            return stan_code
    
    def stan_model_separate_cov(self):

        stan_code = """
                data {
                    int<lower=0> N; // number of observations
                    vector[N] y;    // observations (aggregated)
                    vector[N] i;
                    vector[N] d;
                    int<lower=0> K; // number of groups (conditions)
                    int<lower=1,upper=K> x[N]; // indicators for groups (conditions)
                }
                parameters {
                    real<lower=0> alpha[K];        // pooled alpha (shape)
                    real beta_0[K];
                    real beta_i[K];
                    real beta_d[K];
                }
                model {
                    for (k in 1:K){
                        alpha[k] ~ normal(0, 10);
                        beta_0[k] ~ normal(0, 10);
                        beta_i[k] ~ normal(0, 10);
                        beta_d[k] ~ normal(0, 10);
                    }

                    for (n in 1:N){
                        y[n] ~ weibull(alpha[x[n]], exp(-(beta_0[x[n]] + beta_i[x[n]]*i[n] + beta_d[x[n]]*d[n])/alpha[x[n]]));  // likelihood / observation model
                    }
                }

                generated quantities {
                    vector[N] log_lik;
                    vector[N] y_rep;
                    int<lower = 0, upper = 1> mean_gt;
                    int<lower = 0, upper = 1> sd_gt;
                    for (n in 1:N){
                        log_lik[n] = weibull_lpdf(y[n] | alpha[x[n]], exp(-(beta_0[x[n]] + beta_i[x[n]]*i[n] + beta_d[x[n]]*d[n])/alpha[x[n]])); 
                        y_rep[n] = weibull_rng(alpha[x[n]], exp(-(beta_0[x[n]] + beta_i[x[n]]*i[n] + beta_d[x[n]]*d[n])/alpha[x[n]]));
                        }
                    mean_gt = mean(y_rep) > mean(y);
                    sd_gt = sd(y_rep) > sd(y);
                }


                """
        
        return stan_code