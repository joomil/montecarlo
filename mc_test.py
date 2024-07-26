import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

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

        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = sharpe_ratio
        results[3,i] = i

    return results, weights_record

# Find portfolio by volatility
def find_portfolio_by_volatility(results, weights_record, tickers, target_volatility):
    volatilities = results[1]
    index_closest = np.abs(volatilities - target_volatility).argmin()
    allocation = weights_record[index_closest]
    annualized_return = results[0,index_closest]
    annualized_volatility = results[1,index_closest]

    print(f"Portfolio closest to the target volatility ({target_volatility}):")
    print(f"Annualized Return: {annualized_return:.2%}")
    print(f"Annualized Volatility: {annualized_volatility:.2%}")
    for i, ticker in enumerate(tickers):
        print(f"{ticker}: {allocation[i]:.2%}")

# Parameters
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META']
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

# Find and display the portfolio closest to the given volatility
find_portfolio_by_volatility(results, weights_record, tickers, target_volatility)