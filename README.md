# Paper-Trading Price Monitor

Small personal project: pull daily prices, store them in SQLite, apply simple rules, and
**simulate** buy/sell signals (paper trading). It never places real orders and needs no broker login.

## What it does
- Fetches daily closes (`yahoo` via yfinance, or `synthetic` random-walk data for offline demos)
- Stores prices and simulated trades in SQLite (`monitor.db`)
- Rules (configurable in `config.json`): buy when price is X% below its 20-day average,
  sell on take-profit or stop-loss
- Plots prices, moving average and simulated buy/sell markers to `docs/demo.png`

## Run
```bash
pip install -r requirements.txt
python -m src.monitor --provider yahoo        # real prices
python -m src.monitor --provider synthetic    # offline demo, NOT real market data
pytest
```

## Notes
- Paper trading only. Not financial advice, and the rules are deliberately simple.
- Broker integration (e.g. Trade Republic) is a possible later step; it has no official
  public API for retail accounts, so this version stays on public market data.
- Next ideas: scheduled runs, e-mail alerts, a Power BI dashboard on top of the SQLite tables.
