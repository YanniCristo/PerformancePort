import pandas as pd
import numpy as np

# Carico i dati
np.random.seed(42)

dates = pd.date_range(start="2018-01-01", end="2023-12-31", freq='B')
tickers = ['S&P', 'EuroStoxx600', 'Nasdaq']

data = pd.DataFrame(index=dates, columns=tickers)
for t in tickers:
    returns = np.random.normal(loc=0.0005, scale=0.02, size=len(dates))  # rendimenti giornalieri
    data[t] = (1 + pd.Series(returns, index=dates)).cumprod()  # prezzo simulato cumulativo
