"""Market data providers. Each returns a DataFrame indexed by date with a 'close' column."""
import zlib
import numpy as np
import pandas as pd


def yahoo(ticker: str, days: int = 250) -> pd.DataFrame:
    """Real daily prices via the public yfinance package (no broker account needed)."""
    import yfinance as yf
    df = yf.download(ticker, period=f"{days}d", interval="1d", progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError(f"No data for {ticker}")
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close.rename("close").to_frame()


def synthetic(ticker: str, days: int = 250) -> pd.DataFrame:
    """Random-walk prices for offline demos and tests. NOT real market data."""
    rng = np.random.default_rng(zlib.crc32(ticker.encode()))
    returns = rng.normal(0.0003, 0.015, days)
    prices = 100 * np.exp(np.cumsum(returns))
    idx = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=days)
    return pd.DataFrame({"close": prices}, index=idx)


PROVIDERS = {"yahoo": yahoo, "synthetic": synthetic}
