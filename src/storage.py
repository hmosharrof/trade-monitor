import sqlite3
import pandas as pd


def save(db_path: str, prices: pd.DataFrame, trades: pd.DataFrame, ticker: str):
    with sqlite3.connect(db_path) as con:
        p = prices[["close"]].reset_index()
        p.columns = ["date", "close"]
        p["ticker"] = ticker
        p.to_sql("prices", con, if_exists="append", index=False)
        if not trades.empty:
            t = trades.copy()
            t["ticker"] = ticker
            t.to_sql("simulated_trades", con, if_exists="append", index=False)
