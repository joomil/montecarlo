import yfinance as yf
import pandas as pd
import numpy as np

def fetch_historical_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)
    return hist

def calculate_metrics(hist, risk_free_rate=0.01):
    # Calculate daily returns
    daily_returns = hist['Close'].pct_change().dropna()
    
    # Calculate annualized return
    annualized_return = daily_returns.mean() * 252
    
    # Calculate annualized volatility
    annualized_volatility = daily_returns.std() * np.sqrt(252)
    
    # Calculate Sharpe Ratio
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
    
    # Calculate Sortino Ratio
    downside_returns = daily_returns[daily_returns < 0]
    downside_volatility = downside_returns.std() * np.sqrt(252)
    sortino_ratio = (annualized_return - risk_free_rate) / downside_volatility
    
    # Calculate Information Ratio (assuming SPY as benchmark)
    benchmark = yf.Ticker('SPY').history(start=hist.index[0], end=hist.index[-1])
    benchmark_returns = benchmark['Close'].pct_change().dropna()
    excess_returns = daily_returns - benchmark_returns
    tracking_error = excess_returns.std() * np.sqrt(252)
    information_ratio = (annualized_return - benchmark_returns.mean() * 252) / tracking_error
    
    metrics = {
        'Annualized Return': annualized_return,
        'Annualized Volatility': annualized_volatility,
        'Sharpe Ratio': sharpe_ratio,
        'Sortino Ratio': sortino_ratio,
        'Information Ratio': information_ratio
    }
    return metrics

def main():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
    start_date = '2020-01-01'
    end_date = '2023-01-01'
    risk_free_rate = 0.01
    
    for ticker in tickers:
        print(f"\nFetching data for {ticker}...\n")
        
        # Fetch historical data
        hist_data = fetch_historical_data(ticker, start_date, end_date)
        print(f"Historical Data for {ticker}:\n", hist_data.head(), "\n")
        
        # Calculate metrics
        metrics = calculate_metrics(hist_data, risk_free_rate)
        print(f"Metrics for {ticker}:\n", metrics, "\n")

if __name__ == "__main__":
    main()
