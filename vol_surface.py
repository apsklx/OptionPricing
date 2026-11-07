'''
Module for calculating implied volatility for a range of data
and printing it on a volatility surface
'''

import live_data as ld
import imp_vol as iv
import matplotlib.pyplot as plt
import numpy as np

stock = "^SPX"

stock_list = ld.calls_list(stock)
K = stock_list.iloc[0]['strike']

#hardcoded risk free interest rate
r = 0.0427

def get_data(stock_list, datatype: str):

    series = stock_list[datatype]
    
    if datatype == 'T':
        series = series * 365
        
    return series.tolist()




fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
x = get_data(stock_list, "strike")
y = get_data(stock_list, 'T')
z = get_data(stock_list, 'impliedVolatility')
# 3D Scatter plot for discrete data
surf = ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')

ax.set_title('3D Scatter Plot')
ax.set_xlabel('Strike Price (x-axis)')
ax.set_ylabel('Time to maturity (y-axis)')
ax.set_zlabel('Implied volatility (z-axis)')

# Add a color bar mapping to the Z values
fig.colorbar(surf, ax=ax, label='Implied Volatility')

plt.show()
