import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import random

# Fetch historical data
def fetch_historical_data(tickers, start_date, end_date):
    stock_data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return stock_data

# Calculate daily returns
def calculate_daily_returns(stock_data):
    daily_returns = stock_data.pct_change().dropna()
    return daily_returns

# Simulate portfolio allocations
def simulate_portfolios(daily_returns, num_portfolios=5000, risk_free_rate=0.01):
    num_assets = len(daily_returns.columns)
    results = np.zeros((4, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)

        portfolio_return = np.sum(daily_returns.mean() * weights) * 252
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(daily_returns.cov() * 252, weights)))
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std_dev

        results[0, i] = portfolio_return
        results[1, i] = portfolio_std_dev
        results[2, i] = sharpe_ratio
        results[3, i] = i

    return results, weights_record

# Find portfolios by volatility range
def find_portfolios_by_volatility_range(results, weights_record, tickers, target_volatility, num_portfolios=3):
    volatilities = results[1]
    
    # Calculate the absolute differences from the target volatility
    differences = np.abs(volatilities - target_volatility)
    
    # Get the indices of the portfolios with the smallest differences
    closest_indices = np.argsort(differences)[:num_portfolios]
    
    if len(closest_indices) == 0:
        print(f"No portfolios found close to the target volatility ({target_volatility:.2%})")
        return
    
    print(f"Top {num_portfolios} portfolios closest to the target volatility ({target_volatility}):")
    for index in closest_indices:
        allocation = weights_record[index]
        annualized_return = results[0, index]
        annualized_volatility = results[1, index]

        print(f"\nPortfolio {index + 1}:")
        print(f"Annualized Return: {annualized_return:.2%}")
        print(f"Annualized Volatility: {annualized_volatility:.2%}")
        for i, ticker in enumerate(tickers):
            print(f"{ticker}: {allocation[i]:.2%}")

# Parameters
tickers = ['AAPL','MSFT','GOOGL','AMZN','NVDA','META','TSLA','BRK-B','UNH','JNJ','V','JPM','WMT','PG','MA','HD','BAC','XOM','PFE','KO','DIS','PEP','CSCO','MRK','ABT','COST','CMCSA','ADBE','NFLX','INTC','CRM','AVGO','TXN','ACN','NEE','MDT','NKE','LLY','ORCL','PM']
start_date = '2020-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

# Fetch historical data
stock_data = fetch_historical_data(tickers, start_date, end_date)

# Calculate daily returns
daily_returns = calculate_daily_returns(stock_data)

# Simulate portfolio allocations
results, weights_record = simulate_portfolios(daily_returns)

# Get target volatility from user
target_volatility = float(input("Enter the target volatility: "))

# Find and display the portfolios closest to the given volatility within the range
find_portfolios_by_volatility_range(results, weights_record, tickers, target_volatility)