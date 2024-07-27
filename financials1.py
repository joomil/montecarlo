import yfinance as yf
import pandas as pd

def fetch_historical_data(ticker, period="1y"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

def fetch_company_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

def fetch_financials(ticker):
    stock = yf.Ticker(ticker)
    financials = {
        "Income Statement": stock.financials,
        "Quarterly Income Statement": stock.quarterly_financials,
        "Balance Sheet": stock.balance_sheet,
        "Quarterly Balance Sheet": stock.quarterly_balance_sheet,
        "Cash Flow": stock.cashflow,
        "Quarterly Cash Flow": stock.quarterly_cashflow
    }
    return financials

def fetch_key_metrics(ticker):
    stock = yf.Ticker(ticker)
    metrics = {
        "Sector": stock.info.get('sector'),
        "Trailing P/E": stock.info.get('trailingPE'),
        "Beta": stock.info.get('beta'),
        "Market Cap": stock.info.get('marketCap'),
        "Dividend Yield": stock.info.get('dividendYield')
    }
    return metrics

def main():
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    period = "1y"
    
    for ticker in tickers:
        print(f"\nFetching data for {ticker}...\n")
        
        # Fetch historical data
        hist_data = fetch_historical_data(ticker, period)
        print(f"Historical Data for {ticker}:\n", hist_data.head(), "\n")
        
        # Fetch company info
        company_info = fetch_company_info(ticker)
        print(f"Company Info for {ticker}:\n", company_info, "\n")
        
        # Fetch financials
        financials = fetch_financials(ticker)
        for key, value in financials.items():
            print(f"{key} for {ticker}:\n", value.head(), "\n")
        
        # Fetch key metrics
        key_metrics = fetch_key_metrics(ticker)
        print(f"Key Metrics for {ticker}:\n", key_metrics, "\n")

if __name__ == "__main__":
    main()
