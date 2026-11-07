import numpy as np 

def m_carlo(S0, r, sigma, T, n_simulation, n_steps):
    dt = T/n_steps
    Z = np.random.normal(0,1, [n_simulation,n_steps])
    step_multipliers = np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt)*Z)
    S = np.zeros((n_simulation, n_steps + 1))

    S[:,0] = S0
    S[:, 1:] = S0 * np.cumprod(step_multipliers, axis=1)
    payoff = np.maximum(S[:, -1]-K, 0)
    return np.exp(-r*T)*np.mean(payoff)