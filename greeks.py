'''
Docstring for greeks
'''

import live_data as ld
from scipy.stats import norm
import math
from black_scholes import d1

def vega(S, K,T,r,sigma):
    return S * norm.pdf(d1(S,K,T,r, sigma))*math.sqrt(T)



stock = "LULU"

stock_list = ld.calls_list(stock)
K = stock_list.iloc[0]['strike']
sigma = stock_list.iloc[0]['impliedVolatility']
r = 0.0427
S = ld.get_s(stock)
T = ld.time_to_expiry(stock_list.iloc[0]['expiry'])
market_price = stock_list.iloc[0]['mid']
