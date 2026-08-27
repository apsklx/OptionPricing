'''
Docstring for imp_vol

Implied volatility
'''

from black_scholes import black_scholes
from greeks import vega
import math

eps = 0.00001 #tolerance
sigma_guess = 0.3 #volatility guess
theoretical_price = 126.85955254585951

def f(S,K,T,r,sigma, price):
    return black_scholes(S,K,T,r,sigma) - price

def nr_volatility(S, K, T, r, sigma_guess):
    if abs(f(S, K, T, r, sigma_guess, theoretical_price)) < eps:
        return sigma_guess
    else:
        v = vega(S,K,T,r, sigma_guess)
        if v == 0:
            raise ValueError("Cannot divide by zero!")
        diff = f(S,K, T, r, sigma_guess, theoretical_price)
        sigma_guess = sigma_guess - diff/v
        return nr_volatility(S,K,T,r,sigma_guess)
    
S, K, T, r = 2500, 2500, 1, 0.05

print(nr_volatility(S,K,T,r, sigma_guess))