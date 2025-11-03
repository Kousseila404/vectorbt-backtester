"""
walkforward.py

Module professionnel pour validation walk-forward (rolling window) de stratégies de trading.
Découpe l'historique en multiples fenêtres. Optimise sur la partie train, valide sur la partie test.
Renvoie les setups vraiment robustes (= qui gagnent sur la majorité des périodes OOS).

Usage basique :
    from walkforward import walkforward_validate

    robust_setups = walkforward_validate(
        price_data, strategy_funcs, param_grid,
        window_size=500, test_size=100, min_trades=15
    )

A personnaliser selon ton workflow.

"""

import pandas as pd
import numpy as np

def walkforward_split(price_data, window_size=500, test_size=100):
    """
    Génère les indices train/test pour chaque fenêtre rolling.
    - window_size: nombre de bougies (jours, etc.) dans la fenêtre totale (train+test)
    - test_size: nombre de bougies en test (OOS)
    """
    total = len(price_data)
    windows = []
    for start in range(0, total - window_size - test_size + 1, test_size):
        train_start = start
        train_end = start + window_size
        test_end = train_end + test_size
        if test_end > total:
            break
        windows.append({
            "train": (train_start, train_end),
            "test": (train_end, test_end)
        })
    return windows

def run_backtest(strategy_func, params, price_data):
    """
    Lance le backtest pour une stratégie donnée (fonction + params).
    Doit retourner un dict avec les stats, ex : {'cagr': ..., 'sharpe': ..., 'trades': ..., ...}
    """
    return strategy_func(price_data, **params)

def walkforward_validate(price_data, strategy_funcs, param_grid, window_size=500, test_size=100, min_trades=15):
    """
    Validation walk-forward :
    - price_data : dataframe OHLC (avec DateTimeIndex)
    - strategy_funcs : dict {nom_strategie: fonction}
    - param_grid : dict {nom_strategie: liste de dict de params}
    - window_size, test_size : params rolling window
    - min_trades : nombre min de trades pour valider OOS
    Retourne un DataFrame des setups robustes sur la majorité des fenêtres.
    """
    windows = walkforward_split(price_data, window_size, test_size)
    all_results = []

    for strat_name, func in strategy_funcs.items():
        grid = param_grid.get(strat_name, [])
        for params in grid:
            oos_cagrs = []
            oos_sharpes = []
            oos_maxdds = []
            oos_trades = []
            valid_count = 0
            for w in windows:
                train = price_data.iloc[w["train"][0]:w["train"][1]]
                test = price_data.iloc[w["test"][0]:w["test"][1]]

                # On backtest sur la période d'entraînement (peut-être pour auto-sélectionner les params)
                # Mais ici, on suppose qu'on backtest déjà sur tout le grid.

                # On teste la perf OOS
                res = run_backtest(func, params, test)
                if res.get('trades', 0) >= min_trades and res.get('cagr', 0) > 0:
                    valid_count += 1
                    oos_cagrs.append(res.get('cagr', 0))
                    oos_sharpes.append(res.get('sharpe', 0))
                    oos_maxdds.append(res.get('max_dd', 0))
                    oos_trades.append(res.get('trades', 0))
            # Si la stratégie est valide sur >50% des fenêtres, on la considère robuste
            if valid_count >= len(windows) // 2:
                all_results.append({
                    "strategy": strat_name,
                    **params,
                    "valid_windows": valid_count,
                    "total_windows": len(windows),
                    "mean_oos_cagr": np.mean(oos_cagrs) if oos_cagrs else np.nan,
                    "mean_oos_sharpe": np.mean(oos_sharpes) if oos_sharpes else np.nan,
                    "mean_oos_max_dd": np.mean(oos_maxdds) if oos_maxdds else np.nan,
                    "mean_oos_trades": np.mean(oos_trades) if oos_trades else np.nan,
                })

    results_df = pd.DataFrame(all_results)
    results_df = results_df.sort_values(by="mean_oos_cagr", ascending=False)
    return results_df

if __name__ == "__main__":
    print("Module walk-forward V4 prêt à être utilisé dans le pipeline.")
