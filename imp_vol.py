'''
Docstring for imp_vol

Implied volatility
'''

from black_scholes import black_scholes
from greeks import vega
import math

eps = 0.0000001 #tolerance

def f(S,K,T,r, market_price, sigma):
    return black_scholes(S,K,T,r,sigma) - market_price

#using put call parity here
def sigma_guess(C, S, K, T, r):
    '''
    C float: call option asset price
    S float: underlying asset price
    K float: strike price
    T float: time to maturity
    r float: risk free interest rate
    '''

    X = K * math.exp(-r * T)
    
    term1 = math.sqrt(2 * math.pi) / ((S + X) * math.sqrt(T))
    term2 = C - (S - X) / 2.0
    term3 = term2**2 - ((S - X)**2) / math.pi
        
    return term1 * (term2 + math.sqrt(term3))


def nr_volatility(S, K, T, r, market_price, sigma_guess, max_iter=100, eps=1e-5):
    sigma = sigma_guess
    #arbitrage check (option price cannot be less than intrinsic value)
    intrinsic_value = max(0, S - K * math.exp(-r * T))
    if market_price < intrinsic_value:
        return 0.0
    for _ in range(max_iter):
        


        # f(S,K,T,r,market_price,sigma) = black_scholes(...) - market_price
        price_diff = f(S, K, T, r, market_price, sigma)
        
        if abs(price_diff) <= eps:
            return sigma
        
        v = vega(S, K, T, r, sigma)

        step = price_diff/v
        #we restrict the maximum shift in volatility by %100 either up or down
        step = max(-1, min(1, step))

        if v < 1e-8:
            sigma = sigma + 0.1
            continue  # Avoid division by close to zero values; return 0 for this point on the surface
            
        sigma = sigma - step
        
        # Volatility cannot be negative. If Newton-Raphson overshoots, reset to a small positive number
        if sigma <= 0:
            sigma = abs(sigma)

    return 0  # Did not converge within max_iter   