'''
Docstring for greeks
'''
from scipy.stats import norm
import math
from black_scholes import d1

def vega(S, K,T,r,sigma):
    return S * norm.pdf(d1(S,K,T,r, sigma))*math.sqrt(T)
