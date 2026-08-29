'''
Module for calculating implied volatility for a range of data
and printing it on a volatility surface
'''

from imp_vol import nr_volatility
import matplotlib.pyplot as plt
import numpy as np
import black_scholes


def IV_data(K_data, T_data, S, r):
    '''
    A function that takes Strike price data (K) and Time to expire (T) of a stock
    and returns implied volatility for each of the combination of K and T
    
    :list K_data: Strike prices of a stock (X axis)
    :lost T_data: Time to expire of a stock (Y axis)
    :param S: Current stock price
    :param r: interest free rate
    '''

    K_grid, T_grid = np.meshgrid(K_data, T_data) #because we need a polygon mesh (2d) to draw a 3d surface
    Z = np.zeros_like(K_grid) #array of the same shape and type as K_grid but filled with 0s

    for i in range(K_grid.shape[0]): #range of all possible Strike values
        for j in range(K_grid.shape[1]): #each strike value
            K_current = K_grid[i,j] 
            T_current = T_grid[i,j]
            market_price = black_scholes.black_scholes(S, K_current, T_current, r, 0.20)
            try:
                Z[i,j] = nr_volatility(S, K_current, T_current, r, market_price, 0.3)
            except:
                Z[i,j] = np.nan 
    return K_grid, T_grid, Z

fig = plt.figure(figsize=(10, 7))
ax = plt.axes(projection='3d')

calculated_data = IV_data(np.linspace(0, 280, 50), np.linspace(0.1, 2.0, 50), 140, 0.05)
# Using the generated matrices
surf = ax.plot_surface(calculated_data[0], calculated_data[1], calculated_data[2], cmap='viridis', edgecolor='none')

ax.set_title('Implied Volatility Surface')
ax.set_xlabel('Strike Price (K)')
ax.set_ylabel('Time to Maturity (T)')
ax.set_zlabel('Implied Volatility (σ)')

fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
plt.show()