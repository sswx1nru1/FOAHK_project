# import pandas as pd
# import numpy as np
# from pathlib import Path

# asset_class_returns = {}

# total_cap = 150_000_000
# port_weights = {
#     "Cash": 0.10,
#     "Global_Equities": 0.30,
#     "Fixed_Income": 0.25,
#     "Venture_Capital": 0.10,
#     "Private_Equity": 0.10,
#     "Hedge_Funds": 0.10,
#     "Private_Debt": 0.04,
#     "Digital_Assets": 0.01
# }

# asset_class_tickers = {
#     "Cash": ["BIL", "^IRX"],
#     "Global_Equities": ["ACWI", "SPY", "QQQ", "SMH"],
#     "Fixed_Income": ["AGG", "IEF"],
#     "Venture_Capital": ["ARKK", "QQQ"],
#     "Private_Equity": ["PSP", "KKR", "BX"],
#     "Hedge_Funds": ["QAI", "DBMF", "KMLM"],
#     "Private_Debt": ["BIZD", "ARCC"],
#     "Digital_Assets": ["BTC-USD", "ETH-USD"]
# }

# prices_path = Path(r"C:\Users\xinru\OneDrive\Coding stuff\First try at trading bot\.venv\FOAHK\files\asset_prices.csv")
# prices = pd.read_csv(prices_path, index_col=0, parse_dates=True)
# # returns = prices.pct_change().dropna()
# prices = prices[prices.index >= "2019-01-01"]
# returns = prices.pct_change().dropna()

# for asset_class, tickers in asset_class_tickers.items():
#     available = [t for t in tickers if t in returns.columns]
#     asset_class_returns[asset_class] = returns[available].mean(axis=1)

# asset_class_returns = pd.DataFrame(asset_class_returns)

# # expected returns 
# trading_days = 252
# portfolio_daily_returns = asset_class_returns.mul(port_weights).sum(axis=1)
# # portfolio_log_returns = np.log(1 + portfolio_daily_returns)
# # portfolio_return_1y = np.exp(portfolio_log_returns.mean() * trading_days) - 1
# # portfolio_return_5y = np.exp(portfolio_log_returns.mean() * trading_days * 5) - 1
# portfolio_cumulative = (1 + portfolio_daily_returns).cumprod()
# n_days = portfolio_cumulative.shape[0]
# years = n_days / trading_days
# portfolio_cagr = (portfolio_cumulative.iloc[-1] ** (1 / years)) - 1
# portfolio_return_1y = portfolio_cagr
# portfolio_return_5y = (1 + portfolio_cagr) ** 5 - 1
# portfolio_value_1y = total_cap * (1 + portfolio_return_1y)
# portfolio_value_5y = total_cap * (1 + portfolio_return_5y)

# # print("\n=== Expected Annual Returns by Asset Class ===")
# # print(expected_1y.sort_values(ascending=False))
# # print("\n=== Expected 5-Year Returns by Asset Class ===")
# # print(expected_5y.sort_values(ascending=False))
# print("\n=== Portfolio-Level Expectations ===")
# print(f"Expected 1-Year Return: {portfolio_return_1y:.2%}")
# print(f"Expected 1-Year Value:  ${portfolio_value_1y:,.0f}")
# print(f"\nExpected 5-Year Return: {portfolio_return_5y:.2%}")
# print(f"Expected 5-Year Value:  ${portfolio_value_5y:,.0f}")


import pandas as pd
import numpy as np

# load prices
path = r"C:\Users\xinru\OneDrive\Coding stuff\First try at trading bot\.venv\FOAHK\files\asset_prices.csv"
prices = pd.read_csv(path, index_col=0, parse_dates=True).sort_index()

# monthly returns
monthly_prices = prices.resample("ME").last()
monthly_returns = monthly_prices.pct_change().dropna()
# expected returns
one_year_returns = monthly_returns.mean() * 12          # arithmetic
five_year_returns = (1 + monthly_returns).prod() ** (12 / len(monthly_returns)) - 1

# refedine the assets classes and tickers 
ASSETS = {
    "Cash": ["BIL", "^IRX"],
    "Global Equities": ["ACWI", "SPY", "QQQ", "SMH"],
    "Fixed Income": ["AGG", "IEF"],
    "Venture Capital": ["ARKK", "QQQ"],
    "Private Equity": ["PSP", "KKR", "BX"],
    "Hedge Funds": ["QAI", "DBMF", "KMLM"],
    "Private Debt": ["BIZD", "ARCC"],
    "Digital Assets": ["BTC-USD", "ETH-USD"]
}

# estimate expected returns for each asset class
asset_class_returns = []
for asset_class, tickers in ASSETS.items():
    tickers = [t for t in tickers if t in one_year_returns.index]
    if not tickers:
        continue
    # calculate average expected return for the asset class
    one_year = one_year_returns[tickers].mean()
    five_year = five_year_returns[tickers].mean()
    # store results
    asset_class_returns.append({
        "Asset Class": asset_class,
        "1Y Expected Return": one_year,
        "5Y Expected Return": five_year
    })
asset_returns_df = pd.DataFrame(asset_class_returns).set_index("Asset Class")
print(asset_returns_df)

# define portfolio weights
portfolio_weights = {
    "Cash": 0.10,
    "Global Equities": 0.30,
    "Fixed Income": 0.25,
    "Venture Capital": 0.10,
    "Private Equity": 0.10,
    "Hedge Funds": 0.10,
    "Private Debt": 0.04,
    "Digital Assets": 0.01
}
weights = pd.Series(portfolio_weights)

# calculate weighted returns per asset class
asset_returns_df["Weight"] = weights
asset_returns_df["Weighted 1Y Return"] = asset_returns_df["1Y Expected Return"] * asset_returns_df["Weight"]
asset_returns_df["Weighted 5Y Return"] = asset_returns_df["5Y Expected Return"] * asset_returns_df["Weight"]

initial_capital = 150000000 

# calculate portfolio returns using weighted average
portfolio_1y_return = asset_returns_df["Weighted 1Y Return"].sum()
portfolio_5y_return = asset_returns_df["Weighted 5Y Return"].sum()
end_value_1y = initial_capital * (1 + portfolio_1y_return)
end_value_5y = initial_capital * (1 + portfolio_5y_return) ** 5

# output results
print(f"Expected 1Y Portfolio Return: {portfolio_1y_return:.2%}")
print(f"Portfolio Value After 1Y: ${end_value_1y:,.0f}")
print(f"\nExpected Annualized 5Y Return: {portfolio_5y_return:.2%}")
print(f"Portfolio Value After 5Y: ${end_value_5y:,.0f}")






