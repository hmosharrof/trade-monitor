import pandas as pd
from src.strategy import Rules, simulate


def _prices(values):
    idx = pd.bdate_range("2026-01-01", periods=len(values))
    return pd.DataFrame({"close": values}, index=idx)


def test_buys_on_dip_and_takes_profit():
    prices = _prices([100] * 20 + [90, 100, 110])
    trades, _ = simulate(prices, Rules(sma_window=20, buy_below_sma_pct=5, take_profit_pct=8), 1000)
    assert list(trades.side) == ["BUY", "SELL"]
    assert trades.iloc[1]["reason"] == "take profit"


def test_no_trade_without_dip():
    trades, _ = simulate(_prices([100] * 30), Rules(), 1000)
    assert trades.empty
