'''
Black-Scholes formula for option prices.
'''

from scipy.stats import norm
import math

def black_scholes(S, K, T, r, sigma):
    '''
    Docstring for black_scholes
    
    :float S: current stock price
    :float K: strike price
    :float T: time to expire
    :float r: risk free rate of return
    :float sigma: stock volatility
    '''
    numerator = math.log(S/K) + (r + (sigma**2)/2)*T
    denominator = sigma * math.sqrt(T)

    d1 = numerator/denominator
    d2 = (numerator/denominator) - sigma * math.sqrt(T)

    return S * norm.cdf(d1) - K * math.exp(-r * T)*norm.cdf(d2)


