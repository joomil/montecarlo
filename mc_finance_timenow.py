import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_historical_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Adj Close']

def calculate_log_returns(stock_prices):
    log_returns = np.log(stock_prices / stock_prices.shift(1))
    return log_returns[1:]

def simulate_stock_prices(start_price, mean, std_dev, days, iterations):
    simulated_prices = np.zeros((days, iterations))
    simulated_prices[0] = start_price

    for t in range(1, days):
        random_shocks = np.random.normal(mean, std_dev, iterations)
        simulated_prices[t] = simulated_prices[t-1] * np.exp(random_shocks)
    
    return simulated_prices

def plot_simulation(simulated_prices):
    plt.figure(figsize=(10, 6))
    plt.plot(simulated_prices)
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.title('Monte Carlo Simulation of Stock Prices')
    plt.show()

# Parameters
ticker = 'HO.PA'
start_date = '2020-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
days = 252  # Number of trading days in a year
iterations = 10

# Fetch historical data
stock_prices = fetch_historical_data(ticker, start_date, end_date)

# Calculate log returns
log_returns = calculate_log_returns(stock_prices)

# Estimate parameters
mean = log_returns.mean()
std_dev = log_returns.std()

# Simulate future stock prices
start_price = stock_prices[-1]
simulated_prices = simulate_stock_prices(start_price, mean, std_dev, days, iterations)

# Plot the simulation
plot_simulation(simulated_prices)
