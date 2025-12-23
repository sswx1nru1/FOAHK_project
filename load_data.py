import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path

# suggested tickers for each asset class
ASSETS = {
    "Cash": {
        "BIL": "Treasury Bills ETF",
        "^IRX": "13-week T-Bill Rate"
    },
    "Global_Equities": {
        "ACWI": "Global equities",
        "SPY": "US large-cap",
        "QQQ": "AI / tech tilt",
        "SMH": "Semiconductors"
    },
    "Fixed_Income": {
        "AGG": "Core bonds",
        "IEF": "US Treasuries"
    },
    "Venture_Capital": {
        "ARKK": "Disruptive innovation",
        "QQQ": "Growth proxy"
    },
    "Private_Equity": {
        "PSP": "Listed PE firms",
        "KKR": "KKR stock",
        "BX": "Blackstone"
    },
    "Hedge_Funds": {
        "QAI": "Hedge fund replication",
        "DBMF": "Managed futures",
        "KMLM": "Systematic macro"
    },
    "Private_Debt": {
        "BIZD": "BDC ETF",
        "ARCC": "Ares Capital"
    },
    "Digital_Assets": {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum"
    }
}
ALL_TICKERS = list({
    ticker
    for asset_class in ASSETS.values()
    for ticker in asset_class.keys()
})

#load and clean price data from yfinance
def load_prices(tickers, start_date="2015-01-01"):
    data = yf.download(
        tickers,
        start=start_date,
        progress=False,
        auto_adjust=False,
    )

    if isinstance(data.columns, pd.MultiIndex):
        top_levels = list(data.columns.levels[0])
        if "Adj Close" in top_levels:
            prices = data["Adj Close"]
        elif "Close" in top_levels:
            prices = data["Close"]
        else:
            prices = data
    else:
        if "Adj Close" in data.columns:
            prices = data["Adj Close"]
        elif "Close" in data.columns:
            prices = data["Close"]
        else:
            prices = data
    return prices.dropna()

# save csv 
def save_prices_to_csv(prices, filename="asset_prices.csv"):
    out_dir = Path(r"C:\Users\xinru\OneDrive\Coding stuff\First try at trading bot\.venv\FOAHK\files")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    prices.to_csv(path)
    print(f"Saved CSV to {path}")
    return path

# call functions
if __name__ == "__main__":
    prices = load_prices(ALL_TICKERS)
    save_prices_to_csv(prices)
    print(f"Saved prices for {len(ALL_TICKERS)} tickers to 'asset_prices.csv'")
    