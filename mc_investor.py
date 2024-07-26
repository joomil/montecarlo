import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import minimize

def fetch_historical_data(tickers, start_date, end_date):
    stock_data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return stock_data

def calculate_daily_returns(stock_data):
    daily_returns = stock_data.pct_change().dropna()
    return daily_returns

def portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    returns = np.sum(mean_returns * weights) * 252
    std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))
    sharpe_ratio = (returns - risk_free_rate) / std_dev
    return returns, std_dev, sharpe_ratio

def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    returns, std_dev, sharpe_ratio = portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate)
    return -sharpe_ratio

def check_sum(weights):
    return np.sum(weights) - 1

def risk_constraint(weights, mean_returns, cov_matrix, max_risk):
    returns, std_dev, sharpe_ratio = portfolio_performance(weights, mean_returns, cov_matrix)
    return max_risk - std_dev

def optimize_portfolio(mean_returns, cov_matrix, risk_free_rate, max_risk):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': check_sum},
                   {'type': 'ineq', 'fun': lambda x: risk_constraint(x, mean_returns, cov_matrix, max_risk)})
    bounds = tuple((0, 1) for asset in range(num_assets))
    result = minimize(negative_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                      method='SLSQP', bounds=bounds, constraints=constraints)
    return result

def plot_simulation(results, weights_record, tickers, investment_amount):
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
    print("Expected Portfolio Value:", investment_amount * (1 + max_sharpe_return))
    print("\n")
    for i, ticker in enumerate(tickers):
        print(f"{ticker}: {max_sharpe_allocation[i]:.2%}")

    print("\nMinimum Volatility Portfolio Allocation\n")
    print("Annualized Return:", min_vol_return)
    print("Annualized Volatility:", min_vol_std_dev)
    print("Expected Portfolio Value:", investment_amount * (1 + min_vol_return))
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

def main():
    # Parameters
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    start_date = '2020-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')
    risk_free_rate = 0.01
    max_risk = 0.15  # Maximum acceptable risk (standard deviation)

    # User input for investment amount
    investment_amount = float(input("Enter the amount of investment: "))

    # Fetch historical data
    stock_data = fetch_historical_data(tickers, start_date, end_date)

    # Calculate daily returns
    daily_returns = calculate_daily_returns(stock_data)

    # Estimate parameters
    mean_returns = daily_returns.mean()
    cov_matrix = daily_returns.cov()

    # Optimize portfolio
    result = optimize_portfolio(mean_returns, cov_matrix, risk_free_rate, max_risk)
    optimal_weights = result.x

    # Simulate portfolio allocations
    num_portfolios = 5000
    results = np.zeros((4, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)
        weights_record.append(weights)

        portfolio_return, portfolio_std_dev, sharpe_ratio = portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate)

        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = sharpe_ratio
        results[3,i] = i

    # Plot the simulation results
    plot_simulation(results, weights_record, tickers, investment_amount)

    print("\nOptimal Portfolio Allocation with Risk Constraint\n")
    print("Annualized Return:", portfolio_performance(optimal_weights, mean_returns, cov_matrix, risk_free_rate)[0])
    print("Annualized Volatility:", portfolio_performance(optimal_weights, mean_returns, cov_matrix, risk_free_rate)[1])
    print("Expected Portfolio Value:", investment_amount * (1 + portfolio_performance(optimal_weights, mean_returns, cov_matrix, risk_free_rate)[0]))
    print("\n")
    for i, ticker in enumerate(tickers):
        print(f"{ticker}: {optimal_weights[i]:.2%}")

if __name__ == "__main__":
    main()
