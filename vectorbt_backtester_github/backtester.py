# backtester.py

import yfinance as yf
import vectorbt as vbt
import numpy as np
import pandas as pd
import config
import strategies
from tqdm import tqdm

def load_data(ticker, start, end):
    """
    Télécharge toutes les données OHLCV depuis Yahoo Finance.
    Renvoie le DataFrame complet (Close, Open, High, Low, Volume, etc.).
    """
    data = yf.download(ticker, start=start, end=end)
    # Patch multi-index : aplatis si besoin
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    # Patch : transforme les colonnes tuple en string
    data.columns = [''.join(col) if isinstance(col, tuple) else col for col in data.columns]
    needed_cols = ["Open", "High", "Low", "Close", "Volume"]
    # Vérifie que tout est bien là
    for col in needed_cols:
        if col not in data.columns:
            raise ValueError(f"Colonne {col} manquante dans les données téléchargées")
    data = data.dropna()
    # Index en DatetimeIndex
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)
    return data

def safe_stat(val, fallback=0):
    """Remplace NaN ou valeurs non valides par fallback."""
    import numpy as np
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return fallback
    return val

def run_backtests(price_data, setups, trend_labels, config):
    """
    Lance les backtests pour chaque setup de chaque stratégie.
    Renvoie un DataFrame avec toutes les stats.
    """
    results = []

    # Pour chaque stratégie du dico
    for strat_name, strat_func in strategies.STRATEGY_FUNCS.items():
        for setup in tqdm(setups, desc=f"{strat_name} setups"):
            try:
                # Appelle la fonction stratégie avec le setup (gère les params via **setup)
                entries, exits = strat_func(price_data, **setup)
                # Option : entries = entries & (trend_labels == 1)  # filtrage contexte
                pf = vbt.Portfolio.from_signals(
                    price_data,
                    entries,
                    exits,
                    sl_stop=setup.get("sl_pct", None),
                    tp_stop=setup.get("tp_pct", None),
                    freq="1D"
                )
                stats = pf.stats()
                results.append({
                    "strategy": strat_name,
                    **setup,
                    "trades": safe_stat(stats.get("Total Trades", np.nan)),
                    "cagr": safe_stat(stats.get("CAGR", np.nan)),
                    "sharpe": safe_stat(stats.get("Sharpe Ratio", np.nan)),
                    "max_dd": safe_stat(stats.get("Max Drawdown", np.nan), fallback=-1),
                    "pf": safe_stat(stats.get("Profit Factor", np.nan))
                })
            except Exception as e:
                continue
    return pd.DataFrame(results)
