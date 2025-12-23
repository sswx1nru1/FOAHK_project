import pandas as pd
import numpy as np
from pathlib import Path
from scipy.optimize import minimize

prices = pd.read_csv(
    r"C:\Users\xinru\OneDrive\Coding stuff\First try at trading bot\.venv\FOAHK\files\asset_prices.csv",
    index_col=0,
    parse_dates=True
)
returns = np.log(prices / prices.shift(1)).dropna()

ASSETS = {
    "Cash": ["BIL", "^IRX"],
    "Global_Equities": ["ACWI", "SPY", "QQQ", "SMH"],
    "Fixed_Income": ["AGG", "IEF"],
    "Venture_Capital": ["ARKK", "QQQ"],
    "Private_Equity": ["PSP", "KKR", "BX"],
    "Hedge_Funds": ["QAI", "DBMF", "KMLM"],
    "Private_Debt": ["BIZD", "ARCC"],
    "Digital_Assets": ["BTC-USD", "ETH-USD"],
}

asset_class_returns = {}
for asset_class, tickers in ASSETS.items():
    available = [t for t in tickers if t in returns.columns]
    asset_class_returns[asset_class] = returns[available].mean(axis=1)

asset_class_returns = pd.DataFrame(asset_class_returns)

ANN_FACTOR = 252
mu = asset_class_returns.mean() * ANN_FACTOR
cov = asset_class_returns.cov() * ANN_FACTOR

RISK_FREE_RATE = 0.03  # 3%, conservative proxy
def negative_sharpe(weights, mu, cov, rf):
    portfolio_return = weights @ mu
    portfolio_vol = np.sqrt(weights.T @ cov @ weights)
    return -(portfolio_return - rf) / portfolio_vol

n = len(mu)
constraints = (
    {"type": "eq", "fun": lambda w: np.sum(w) - 1}
)
bounds = [(0, 1) for _ in range(n)]
w0 = np.ones(n) / n

result = minimize(
    negative_sharpe,
    w0,
    args=(mu, cov, RISK_FREE_RATE),
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)
sharpe_weights = pd.Series(result.x, index=mu.index)

def portfolio_stats(weights, mu, cov, rf):
    ret = weights @ mu
    vol = np.sqrt(weights.T @ cov @ weights)
    sharpe = (ret - rf) / vol
    return ret, vol, sharpe
sharpe_ret, sharpe_vol, sharpe_ratio = portfolio_stats(
    sharpe_weights.values, mu, cov, RISK_FREE_RATE
)


print(sharpe_weights.round(4))
print("\nExpected Return:", round(sharpe_ret, 4))
print("Volatility:", round(sharpe_vol, 4))
print("Sharpe Ratio:", round(sharpe_ratio, 4))

current_weights = pd.Series({
    "Cash": 0.10,
    "Global_Equities": 0.30,
    "Fixed_Income": 0.25,
    "Venture_Capital": 0.10,
    "Private_Equity": 0.10,
    "Hedge_Funds": 0.10,
    "Private_Debt": 0.04,
    "Digital_Assets": 0.01,
})[mu.index]
cur_ret, cur_vol, cur_sharpe = portfolio_stats(
    current_weights.values, mu, cov, RISK_FREE_RATE
)
comparison = pd.DataFrame({
    "Current": current_weights,
    "Sharpe_Optimal": sharpe_weights
})

print(comparison)
print("\nCurrent Sharpe:", round(cur_sharpe, 4))
print("Optimised Sharpe:", round(sharpe_ratio, 4))

# also create a percent (×100) version of the comparison and save it
out_dir = Path(r"C:\Users\xinru\OneDrive\Coding stuff\First try at trading bot\.venv\FOAHK\files")
out_dir.mkdir(parents=True, exist_ok=True)
comparison_pct = comparison * 100
comparison_pct_path = out_dir / "weights_comparison_percent.csv"
comparison_pct.to_csv(comparison_pct_path)
print("\nComparison (percent):")
print(comparison_pct.round(2))
print(f"Saved comparison percent CSV to {comparison_pct_path}")

