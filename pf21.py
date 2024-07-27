import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize
from datetime import datetime

# Function to fetch stock data
def fetch_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

# Function to calculate portfolio performance
def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return returns, std

# Function to calculate negative Sharpe ratio
def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_returns, p_std = portfolio_performance(weights, mean_returns, cov_matrix)
    return -(p_returns - risk_free_rate) / p_std

# Function to optimize portfolio
def optimize_portfolio(tickers, start_date, end_date, risk_free_rate=0.01):
    data = fetch_data(tickers, start_date, end_date)
    returns = data.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    num_assets = len(tickers)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    result = minimize(neg_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                      method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result, mean_returns, cov_matrix, returns

# Function to calculate metrics for each asset
def asset_metrics(returns, risk_free_rate=0.01):
    metrics = {}
    for column in returns.columns:
        avg_return = returns[column].mean() * 252
        volatility = returns[column].std() * np.sqrt(252)
        sharpe_ratio = (avg_return - risk_free_rate) / volatility
        metrics[column] = {
            'Average Return': avg_return,
            'Volatility': volatility,
            'Sharpe Ratio': sharpe_ratio
        }
    return metrics

# Main function
if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
               'HO.PA', 'AM.PA', 'DSY.PA', 'SAF.PA', 'AIR.PA'
               ]
    start_date = '2020-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')
    risk_free_rate = 0.01
    
    result, mean_returns, cov_matrix, returns = optimize_portfolio(tickers, start_date, end_date, risk_free_rate)
    optimal_weights = result.x
    
    print("Optimal Weights:")
    for ticker, weight in zip(tickers, optimal_weights):
        print(f"{ticker}: {weight:.4f}")
    
    portfolio_return, portfolio_volatility = portfolio_performance(optimal_weights, mean_returns, cov_matrix)
    portfolio_sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    
    print("\nPortfolio Performance:")
    print(f"Return: {portfolio_return:.4f}")
    print(f"Volatility: {portfolio_volatility:.4f}")
    print(f"Sharpe Ratio: {portfolio_sharpe_ratio:.4f}")
    
    metrics = asset_metrics(returns, risk_free_rate)
    print("\nAsset Metrics:")
    for ticker, metric in metrics.items():
        print(f"{ticker}:")
        print(f"  Average Return: {metric['Average Return']:.4f}")
        print(f"  Volatility: {metric['Volatility']:.4f}")
        print(f"  Sharpe Ratio: {metric['Sharpe Ratio']:.4f}")
