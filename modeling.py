import pandas as pd
import numpy as np
from scipy.optimize import minimize
import statsmodels.api as sm

class MMM():
    def __init__(self, media_vars):
        self.media_vars = media_vars

    def __apply_adstock(self, data, beta):
        adstocked = np.zeros_like(data)
        carryover = 0
        for i in range(len(data)):
            carryover = data[i] + beta * carryover
            adstocked[i] = carryover
        return adstocked
    
    def __apply_diminishing_returns(self, data, alpha):
        return data ** alpha
    
    def __transform_data(self, alphas, betas):
        transformed_data = pd.DataFrame()
        for i, var in enumerate(self.media_vars):
            adstocked = self.__apply_adstock(media_dt[var].values, betas[i])
            transformed_data[var] = self.__apply_diminishing_returns(adstocked, alphas[i])
        return transformed_data

    def __cost_function(self, params, media_dt, media_vars, dependent_var):
        alphas = params[:len(media_vars)]
        betas = params[len(media_vars):]
        y = media_dt[dependent_var].values
        transformed_data = np.zeros_like(media_dt[media_vars].values)
        
        for i, var in enumerate(media_vars):
            adstocked = self.__apply_adstock(media_dt[var].values, betas[i])
            transformed_data[:, i] = self.__apply_diminishing_returns(adstocked, alphas[i])
        
        # Fit regression model
        X = sm.add_constant(transformed_data)
        model = sm.OLS(y, X).fit()
        return -model.rsquared
    
    def optimize_parameters(self, media_dt, media_vars, dependent_var, alpha_bounds=(0, 2), beta_bounds=(0, 1)):
        # Initial guesses for alphas and betas
        initial_guess = [0.5] * len(media_vars) * 2
        bounds = [alpha_bounds] * len(media_vars) + [beta_bounds] * len(media_vars)
        
        # Run optimization
        result = minimize(
            self.__cost_function,
            initial_guess,
            args=(media_dt, media_vars, dependent_var),
            bounds=bounds,
            method="L-BFGS-B"
        )
        
        # Extract optimized alphas and betas
        n_vars = len(media_vars)
        optimized_alphas = result.x[:n_vars]
        optimized_betas = result.x[n_vars:]
        
        return optimized_alphas, optimized_betas, -result.fun
    
    def final_regression(self, media_dt, media_vars, dependent_var, alphas, betas):
        transformed_data = self.__transform_data(media_dt, media_vars, alphas, betas)

        y = media_dt[dependent_var]

        X = sm.add_constant(transformed_data)

        model = sm.OLS(y, X).fit()
        
        return model