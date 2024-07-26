import numpy as np
import matplotlib.pyplot as plt

def simulate_stock_paths(S0, r, sigma, T, M, I):
    """
    Simulate stock price paths using Geometric Brownian Motion.
    
    Parameters:
    S0 : float : initial stock price
    r : float : risk-free rate
    sigma : float : volatility
    T : float : time to maturity
    M : int : number of time steps
    I : int : number of simulations
    
    Returns:
    paths : ndarray : simulated stock price paths
    """
    dt = T / M
    paths = np.zeros((M + 1, I))
    paths[0] = S0
    for t in range(1, M + 1):
        z = np.random.standard_normal(I)
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)
    return paths

def calculate_option_price(S0, K, r, sigma, T, M, I):
    """
    Calculate the price of a European call option using Monte Carlo simulation.
    
    Parameters:
    S0 : float : initial stock price
    K : float : strike price
    r : float : risk-free rate
    sigma : float : volatility
    T : float : time to maturity
    M : int : number of time steps
    I : int : number of simulations
    
    Returns:
    option_price : float : estimated option price
    """
    paths = simulate_stock_paths(S0, r, sigma, T, M, I)
    payoffs = np.maximum(paths[-1] - K, 0)
    option_price = np.exp(-r * T) * np.mean(payoffs)
    return option_price

def plot_simulation(paths):
    """
    Plot the simulated stock price paths.
    
    Parameters:
    paths : ndarray : simulated stock price paths
    """
    plt.figure(figsize=(10, 6))
    plt.plot(paths[:, :10])
    plt.xlabel('Time Steps')
    plt.ylabel('Stock Price')
    plt.title('Simulated Stock Price Paths')
    plt.show()

# Parameters
S0 = 100  # Initial stock price
K = 105  # Strike price
r = 0.05  # Risk-free rate
sigma = 0.2  # Volatility
T = 1.0  # Time to maturity (1 year)
M = 252  # Number of time steps (daily)
I = 10000  # Number of simulations

# Simulate stock price paths
paths = simulate_stock_paths(S0, r, sigma, T, M, I)

# Calculate the option price
option_price = calculate_option_price(S0, K, r, sigma, T, M, I)

# Print the estimated option price
print(f"Estimated European call option price: ${option_price:.2f}")

# Plot the simulated stock price paths
plot_simulation(paths)
