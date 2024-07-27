import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize

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
    
    return result, mean_returns, cov_matrix

# Main function
if __name__ == "__main__":
    # List of French stock tickers (example tickers, you can add more)
    tickers = [
    'AI.PA', 'AIR.PA', 'ALO.PA', 'MT.AS', 'CS.PA', 'BNP.PA', 'EN.PA', 'CAP.PA', 'CA.PA', 'ACA.PA',
    'BN.PA', 'DSY.PA', 'EDEN.PA', 'ENGI.PA', 'EL.PA', 'ERF.PA', 'RMS.PA', 'KER.PA', 'OR.PA', 'LR.PA',
    'MC.PA', 'ML.PA', 'ORA.PA', 'RI.PA', 'PUB.PA', 'RNO.PA', 'SAF.PA', 'SGO.PA', 'SAN.PA', 'SU.PA',
    'GLE.PA', 'STLAP.PA', 'STMPA.PA', 'TEP.PA', 'HO.PA', 'TTE.PA', 'VIE.PA', 'DG.PA', 'WLN.PA', 'UBI.PA']

    start_date = '2020-01-01'
    end_date = '2024-07-25'
    risk_free_rate = 0.01
    
    result, mean_returns, cov_matrix = optimize_portfolio(tickers, start_date, end_date, risk_free_rate)
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
