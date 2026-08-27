'''
Docstring for vol_surface

'''

from imp_vol import nr_volatility
import matplotlib.pyplot as plt
import numpy as np
S = 2500
r = 0.05
Strike = np.linspace(2000, 3000, 50) #Strike prices (X axis)
Time = np.linspace(0.1, 2.0, 50) #Time to matrurity (Y axis)

K_grid, T_grid = np.meshgrid(Strike, Time)
Z = np.zeros_like(K_grid)

for i in range(K_grid.shape[0]):
    for j in range(K_grid.shape[1]):
        K_current = K_grid[i,j]
        T_current = T_grid[i,j]

        intrinsic_value = max(S - K_current, 0)
        time_value = 50 * T_current
        
        target_price = intrinsic_value + time_value
        try:
            Z[i,j] = nr_volatility(S, K_current, T_current, r, target_price)
        except:
            Z[i,j] = np.nan

fig = plt.figure(figsize=(10, 7))
ax = plt.axes(projection='3d')

# Using the generated matrices
surf = ax.plot_surface(K_grid, T_grid, Z, cmap='viridis', edgecolor='none')

ax.set_title('Implied Volatility Surface')
ax.set_xlabel('Strike Price (K)')
ax.set_ylabel('Time to Maturity (T)')
ax.set_zlabel('Implied Volatility (σ)')

fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
plt.show()