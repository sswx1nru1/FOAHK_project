import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load CSV
prices = pd.read_csv(
    r"C:\Users\xinru\OneDrive\Coding stuff\First try at trading bot\.venv\FOAHK\files\asset_prices.csv",
    index_col=0,
    parse_dates=True
)

# Compute log returns
returns = np.log(prices / prices.shift(1)).dropna()

# define asset classes and tickers
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

# calculate average returns per asset class
asset_class_returns = {}
for asset_class, tickers in ASSETS.items():
    available = [t for t in tickers if t in returns.columns]
    asset_class_returns[asset_class] = returns[available].mean(axis=1)

asset_class_returns = pd.DataFrame(asset_class_returns)

# calculate annualized mean and covariance
ANN_FACTOR = 252
mu = asset_class_returns.mean() * ANN_FACTOR
cov = asset_class_returns.cov() * ANN_FACTOR

# define current portfolio weights
current_weights = pd.Series({
    "Cash": 0.10,
    "Global_Equities": 0.30,
    "Fixed_Income": 0.25,
    "Venture_Capital": 0.10,
    "Private_Equity": 0.10,
    "Hedge_Funds": 0.10,
    "Private_Debt": 0.04,
    "Digital_Assets": 0.01,
})
current_weights = current_weights[mu.index]

# define portfolio risk function
def portfolio_volatility(weights, cov):
    return np.sqrt(weights.T @ cov @ weights)

# optimize portfolio to minimize volatility
n = len(mu)

constraints = (
    {"type": "eq", "fun": lambda w: np.sum(w) - 1}
)

bounds = [(0, 1) for _ in range(n)]

w0 = np.ones(n) / n
result = minimize(
    portfolio_volatility,
    w0,
    args=(cov,),
    method="SLSQP",
    bounds=bounds,
    constraints=constraints
)

optimal_weights = pd.Series(result.x, index=mu.index)

# compare current and optimal weights
current_vol = portfolio_volatility(current_weights.values, cov)
optimal_vol = portfolio_volatility(optimal_weights.values, cov)

current_return = current_weights @ mu
optimal_return = optimal_weights @ mu
comparison = pd.DataFrame({
    "Current Weight": current_weights,
    "Optimal Weight": optimal_weights,
})

print(comparison)
print("\nCurrent Volatility:", current_vol)
print("Optimal Volatility:", optimal_vol)
print("\nCurrent Expected Return:", current_return)
print("Optimal Expected Return:", optimal_return)
