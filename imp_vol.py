'''
Docstring for imp_vol

Implied volatility
'''

from black_scholes import black_scholes
from greeks import vega
import numpy as np
import math

eps = 0.00001 #tolerance

def f(S,K,T,r, market_price, sigma):
    return black_scholes(S,K,T,r,sigma) - market_price

def nr_volatility(S, K, T, r, market_price, sigma_guess=0.3, max_iter=100, eps=1e-5):
    sigma = sigma_guess
    
    for _ in range(max_iter):
        # f(S,K,T,r,market_price,sigma) = black_scholes(...) - market_price
        price_diff = f(S, K, T, r, market_price, sigma)
        
        if abs(price_diff) < eps:
            return sigma
            
        v = vega(S, K, T, r, sigma)
        
        if v == 0:
            return np.nan  # Avoid division by zero; return NaN for this point on the surface
            
        sigma = sigma - (price_diff / v)
        
        # Volatility cannot be negative. If Newton-Raphson overshoots, reset to a small positive number
        if sigma <= 0:
            sigma = 1e-5 
            
    return np.nan  # Did not converge within max_iter