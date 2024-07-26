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

# Plot the results
def plot_simulation(results, weights_record, tickers):
    max_sharpe_idx = np.argmax(results[2])
    max_sharpe_allocation = weights_record[int(results[3,max_sharpe_idx])]
    max_sharpe_return = results[0,max_sharpe_idx]
    max_sharpe_std_dev = results[1,max_sharpe_idx]

    min_vol_idx = np.argmin(results[1])
    min_vol_allocation = weights_record[int(results[3,min_vol_idx])]
    min_vol_return = results[0,min_vol_idx]
    min_vol_std_dev = results[1,min_vol_idx]

    print("Maximum Sharpe Ratio Portfolio Allocation\n")
    print("Annualized Return:", max_sharpe_return)
    print("Annualized Volatility:", max_sharpe_std_dev)
    print("\n")
    for i, ticker in enumerate(tickers):
        print(f"{ticker}: {max_sharpe_allocation[i]:.2%}")

    print("\nMinimum Volatility Portfolio Allocation\n")
    print("Annualized Return:", min_vol_return)
    print("Annualized Volatility:", min_vol_std_dev)
    print("\n")
    for i, ticker in enumerate(tickers):
        print(f"{ticker}: {min_vol_allocation[i]:.2%}")

    plt.figure(figsize=(10, 6))
    plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis')
    plt.colorbar(label='Sharpe Ratio')
    plt.scatter(max_sharpe_std_dev, max_sharpe_return, c='red', marker='*', s=200)
    plt.scatter(min_vol_std_dev, min_vol_return, c='blue', marker='*', s=200)
    plt.title('Efficient Frontier')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.show()

# Parameters
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
start_date = '2020-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

# Fetch historical data
stock_data = fetch_historical_data(tickers, start_date, end_date)

# Calculate daily returns
daily_returns = calculate_daily_returns(stock_data)

# Simulate portfolio allocations
results, weights_record = simulate_portfolios(daily_returns)

# Plot the simulation results
plot_simulation(results, weights_record, tickers)
