import pandas as pd

def fetch_cac40_tickers():
    url = "https://en.wikipedia.org/wiki/CAC_40"
    tables = pd.read_html(url)
    # Manually inspect the tables to find the correct one
    for table in tables:
        if 'Ticker' in table.columns:
            return table['Ticker'].tolist()
    return []

def fetch_cac_mid60_tickers():
    url = "https://en.wikipedia.org/wiki/CAC_Mid_60"
    tables = pd.read_html(url)
    # Manually inspect the tables to find the correct one
    for table in tables:
        if 'Ticker' in table.columns:
            return table['Ticker'].tolist()
    return []

def fetch_cac_small_tickers():
    url = "https://en.wikipedia.org/wiki/CAC_Small"
    tables = pd.read_html(url)
    # Manually inspect the tables to find the correct one
    for table in tables:
        if 'Ticker' in table.columns:
            return table['Ticker'].tolist()
    return []

def fetch_sbf250_tickers():
    url = "https://en.wikipedia.org/wiki/SBF_250"
    tables = pd.read_html(url)
    # Manually inspect the tables to find the correct one
    for table in tables:
        if 'Ticker' in table.columns:
            return table['Ticker'].tolist()
    return []

def main():
    # Fetch tickers from different indices
    cac40_tickers = fetch_cac40_tickers()
    cac_mid60_tickers = fetch_cac_mid60_tickers()
    cac_small_tickers = fetch_cac_small_tickers()
    sbf250_tickers = fetch_sbf250_tickers()

    # Combine all tickers into a single list
    all_tickers = list(set(cac40_tickers + cac_mid60_tickers + cac_small_tickers + sbf250_tickers))

    # Print the list of tickers
    print("List of French Tickers:")
    for ticker in all_tickers:
        print(ticker)

    # Optionally, save the list of tickers to a CSV file
    df = pd.DataFrame(all_tickers, columns=["Ticker"])
    df.to_csv("french_tickers.csv", index=False)

if __name__ == "__main__":
    main()
