import numpy as np
import pandas as pd
import yfinance as yf
import concurrent.futures
from datetime import datetime
from scipy.optimize import minimize

# Function to fetch historical data for a single stock
def fetch_stock_data(ticker):
    try:
        return yf.download(ticker, start='2020-01-01', end=datetime.now().strftime('%Y-%m-%d'))['Adj Close']
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure

# Function to fetch historical data for multiple stocks concurrently
def fetch_all_stocks_data(tickers):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all tasks and store them in a dictionary keyed by the ticker symbol
        future_to_ticker = {executor.submit(fetch_stock_data, ticker): ticker for ticker in tickers}
        # Retrieve the results from the futures and store them in a dictionary keyed by the ticker symbol
        data = {}
        for future, ticker in future_to_ticker.items():
            result = future.result()
            if not result.empty:  # Only add non-empty DataFrames to the dictionary
                data[ticker] = result
    return data

# Function to calculate daily returns
def calculate_daily_returns(data):
    return data.pct_change().dropna()

# Function to estimate mean returns and covariance matrix
def estimate_parameters(daily_returns):
    mean_returns = daily_returns.mean()
    cov_matrix = daily_returns.cov()
    return mean_returns, cov_matrix

# Function to compute portfolio performance
def portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    returns = np.sum(mean_returns * weights) * 252
    std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
    sharpe_ratio = (returns - risk_free_rate) / std_dev
    return returns, std_dev, sharpe_ratio

# Function to find the weights that maximize the Sharpe ratio
def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    returns, std_dev, sharpe_ratio = portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate)
    return -sharpe_ratio

# Main function to orchestrate the process
def main():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']  # Add more tickers as needed
    data = fetch_all_stocks_data(tickers)
    
    # Filter out tickers for which data retrieval failed
    valid_tickers = [ticker for ticker, df in data.items() if not df.empty]
    
    # Concatenate data for valid tickers only
    if valid_tickers:
        combined_data = pd.concat([data[ticker] for ticker in valid_tickers], axis=1)
        
        # Calculate daily returns
        daily_returns = calculate_daily_returns(combined_data)
        
        # Estimate mean returns and covariance matrix
        mean_returns, cov_matrix = estimate_parameters(daily_returns)
        
        # Define the optimization problem
        num_assets = len(mean_returns)
        args = (mean_returns, cov_matrix, 0.01)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, None) for _ in range(num_assets))
        
        # Solve the optimization problem
        result = minimize(neg_sharpe_ratio, num_assets*[1./num_assets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
        optimal_weights = result.x
        
        # Print the optimal weights
        for i, ticker in enumerate(valid_tickers):
            print(f"{ticker}: {optimal_weights[i]:.2%}")
    else:
        print("No valid data retrieved for any stocks.")

if __name__ == "__main__":
    main()
