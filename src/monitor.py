"""Paper-trading price monitor. Usage: python -m src.monitor --provider yahoo"""
import argparse, json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.providers import PROVIDERS
from src.strategy import Rules, simulate
from src.storage import save


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=PROVIDERS, default="yahoo")
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--db", default="monitor.db")
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    rules = Rules(cfg["sma_window"], cfg["buy_below_sma_pct"], cfg["take_profit_pct"], cfg["stop_loss_pct"])
    if os.path.exists(args.db):
        os.remove(args.db)
    os.makedirs("docs", exist_ok=True)

    tickers = cfg["tickers"]
    fig, axes = plt.subplots(len(tickers), 1, figsize=(10, 3 * len(tickers)), sharex=False)
    axes = [axes] if len(tickers) == 1 else axes
    print(f"{'Ticker':<8}{'Trades':>7}{'Realized P&L (EUR/USD)':>26}")
    for ax, t in zip(axes, tickers):
        prices = PROVIDERS[args.provider](t)
        trades, df = simulate(prices, rules, cfg["position_size"])
        save(args.db, prices, trades, t)
        pnl = df["realized_pnl"].iloc[-1]
        print(f"{t:<8}{len(trades):>7}{pnl:>26.2f}")
        ax.plot(df.index, df["close"], label=t, lw=1)
        ax.plot(df.index, df["sma"], label=f"SMA{rules.sma_window}", lw=1, ls="--")
        if not trades.empty:
            b, s = trades[trades.side == "BUY"], trades[trades.side == "SELL"]
            ax.scatter(b["date"], b["price"], marker="^", color="green", zorder=3, label="simulated buy")
            ax.scatter(s["date"], s["price"], marker="v", color="red", zorder=3, label="simulated sell")
        ax.set_title(f"{t} - paper trades, source: {args.provider}", fontsize=10)
        ax.legend(fontsize=7, loc="upper left")
    plt.tight_layout()
    plt.savefig("docs/demo.png", dpi=110)
    print("Chart saved to docs/demo.png, data in", args.db)


if __name__ == "__main__":
    main()
