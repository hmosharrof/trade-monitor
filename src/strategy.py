"""Rule-based signals and a paper-trading simulation. No real orders are ever sent."""
from dataclasses import dataclass
import pandas as pd


@dataclass
class Rules:
    sma_window: int = 20
    buy_below_sma_pct: float = 5.0
    take_profit_pct: float = 8.0
    stop_loss_pct: float = 10.0


def simulate(prices: pd.DataFrame, rules: Rules, position_size: float):
    """Walk through daily prices; buy on a dip below the SMA, sell on take-profit or stop-loss.
    Returns (trades, equity_curve). Trades are simulated only."""
    df = prices.copy()
    df["sma"] = df["close"].rolling(rules.sma_window).mean()
    trades, qty, entry = [], 0.0, 0.0
    cash_flow = []
    for date, row in df.iterrows():
        price, sma = row["close"], row["sma"]
        if pd.isna(sma):
            cash_flow.append(0.0)
            continue
        if qty == 0 and price <= sma * (1 - rules.buy_below_sma_pct / 100):
            qty, entry = position_size / price, price
            trades.append({"date": date, "side": "BUY", "price": price, "qty": qty, "reason": "dip below SMA"})
        elif qty > 0:
            change = (price / entry - 1) * 100
            reason = "take profit" if change >= rules.take_profit_pct else "stop loss" if change <= -rules.stop_loss_pct else None
            if reason:
                trades.append({"date": date, "side": "SELL", "price": price, "qty": qty, "reason": reason})
                cash_flow.append((price - entry) * qty)
                qty = 0.0
                continue
        cash_flow.append(0.0)
    df["realized_pnl"] = pd.Series(cash_flow, index=df.index).cumsum()
    return pd.DataFrame(trades), df
