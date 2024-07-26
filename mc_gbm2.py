import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_historical_data(ticker, start_date, end_date):
    """
    Fetch historical stock data using yfinance.
    
    Parameters:
    ticker : str : stock ticker symbol
    start_date : str : start date in YYYY-MM-DD format
    end_date : str : end date in YYYY-MM-DD format
    
    Returns:
    stock_data : pd.DataFrame : historical stock data
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Adj Close']

def calculate_log_returns(stock_prices):
    """
    Calculate the daily log returns of the stock.
    
    Parameters:
    stock_prices : pd.Series : stock prices
    
    Returns:
    log_returns : pd.Series : daily log returns
    """
    log_returns = np.log(stock_prices / stock_prices.shift(1))
    return log_returns[1:]

def simulate_stock_prices(S0, mu, sigma, T, dt, N):
    """
    Simulate stock price paths using Geometric Brownian Motion.
    
    Parameters:
    S0 : float : initial stock price
    mu : float : mean return
    sigma : float : volatility
    T : float : time horizon (in years)
    dt : float : time step (in years)
    N : int : number of simulations
    
    Returns:
    paths : ndarray : simulated stock price paths
    """
    num_steps = int(T / dt)
    paths = np.zeros((num_steps + 1, N))
    paths[0] = S0
    for t in range(1, num_steps + 1):
        z = np.random.standard_normal(N)
        paths[t] = paths[t - 1] * np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)
    return paths

def plot_simulation_and_distribution(paths, final_prices):
    """
    Plot the simulated stock price paths and the distribution of final stock prices.
    
    Parameters:
    paths : ndarray : simulated stock price paths
    final_prices : ndarray : final stock prices from the simulation
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot the simulated stock price paths
    ax1.plot(paths)
    ax1.set_xlabel('Time Steps')
    ax1.set_ylabel('Stock Price')
    ax1.set_title('Monte Carlo Simulation of Stock Prices')

    # Plot the distribution of final stock prices
    ax2.hist(final_prices, bins=50, edgecolor='black')
    ax2.set_xlabel('Final Stock Price')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Final Stock Prices from Monte Carlo Simulation')

    plt.tight_layout()
    plt.show()

# Parameters
ticker = 'AAPL'  # Stock ticker symbol
start_date = '2020-01-01'  # Start date for historical data
end_date = datetime.today().strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
T = 1.0  # Time horizon (1 year)
dt = 1/252  # Time step (1 trading day)
N = 10000  # Number of simulations

# Fetch historical data
stock_prices = fetch_historical_data(ticker, start_date, end_date)

# Calculate log returns
log_returns = calculate_log_returns(stock_prices)

# Estimate parameters
mu = log_returns.mean()
sigma = log_returns.std()

# Simulate future stock prices
S0 = stock_prices[-1]
paths = simulate_stock_prices(S0, mu, sigma, T, dt, N)

# Analyze the results
final_prices = paths[-1]
mean_final_price = np.mean(final_prices)
median_final_price = np.median(final_prices)
lower_confidence = np.percentile(final_prices, 5)
upper_confidence = np.percentile(final_prices, 95)

# Print the results
print(f"Mean final stock price: ${mean_final_price:.2f}")
print(f"Median final stock price: ${median_final_price:.2f}")
print(f"5% confidence interval: ${lower_confidence:.2f} - ${upper_confidence:.2f}")

# Plot the simulation results and the distribution of final stock prices
plot_simulation_and_distribution(paths, final_prices)
