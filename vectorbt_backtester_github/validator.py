

"""
validator.py

Module pour valider les stratégies backtestées de manière "pro" :
- Validation out-of-sample (OOS) : test des meilleurs setups sur une période jamais vue.
- Validation walk-forward : simule le trading "en vrai" sur des fenêtres successives.
- Filtre les setups robustes, évite la suroptimisation.

Usage :
    from validator import validate_setups

    robust_setups = validate_setups(setups_df, price_data, split_ratio=0.7, min_trades=15)

A compléter selon ton workflow.
"""

import pandas as pd
import numpy as np

def split_data(price_data, split_ratio=0.7):
    """Découpe les données prix en in-sample et out-of-sample."""
    split_idx = int(len(price_data) * split_ratio)
    in_sample = price_data.iloc[:split_idx]
    out_sample = price_data.iloc[split_idx:]
    return in_sample, out_sample

def run_backtest_on_period(strategy_func, params, price_data):
    """
    Lance le backtest d'une stratégie (sous forme de fonction) sur price_data.
    Ex: stratégie = moving_average_crossover
        params = {'ma_short': 20, 'ma_long': 100, ...}
    """
    return strategy_func(price_data, **params)

def validate_setups(setups_df, price_data, strategy_funcs=None, split_ratio=0.7, min_trades=15):
    """
    Pour chaque setup gagnant, teste sa robustesse out-of-sample.
    - setups_df: DataFrame des setups à valider (issus du backtest principal)
    - price_data: Données OHLC complètes
    - strategy_funcs: dict {stratégie: fonction}
    - split_ratio: % données pour l'in-sample (reste en OOS)
    - min_trades: nombre min de trades en OOS pour considérer le setup comme valide

    Retourne un DataFrame des setups robustes (OOS).
    """
    results = []

    in_sample, out_sample = split_data(price_data, split_ratio)

    for idx, setup in setups_df.iterrows():
        strat_type = setup.get('strategy_type', 'moving_average_crossover')
        params = {k: setup[k] for k in setup.index if k not in ['trades', 'cagr', 'sharpe', 'max_dd', 'pf', 'strategy_type']}

        # 1. Run sur in-sample pour vérifier les perfs initiales
        if strategy_funcs and strat_type in strategy_funcs:
            strategy_func = strategy_funcs[strat_type]
        else:
            continue  # Skip si pas de fonction associée

        res_in = run_backtest_on_period(strategy_func, params, in_sample)
        res_out = run_backtest_on_period(strategy_func, params, out_sample)

        if res_out['trades'] >= min_trades:
            # Filtre anti-suroptimisation : on garde ceux qui ne s'effondrent pas OOS
            ratio = res_out['cagr'] / res_in['cagr'] if res_in['cagr'] else np.nan
            robust = ratio > 0.5 and res_out['cagr'] > 0  # Ex : CAGR OOS doit être >0 et >50% de l'in
            results.append({
                **params,
                'strategy_type': strat_type,
                'trades_in': res_in['trades'],
                'cagr_in': res_in['cagr'],
                'sharpe_in': res_in['sharpe'],
                'max_dd_in': res_in['max_dd'],
                'pf_in': res_in['pf'],
                'trades_out': res_out['trades'],
                'cagr_out': res_out['cagr'],
                'sharpe_out': res_out['sharpe'],
                'max_dd_out': res_out['max_dd'],
                'pf_out': res_out['pf'],
                'robust': robust,
                'robust_ratio': ratio
            })

    robust_df = pd.DataFrame(results)
    robust_df = robust_df[robust_df['robust']]
    return robust_df

# À compléter : Ajoute ici la logique walk-forward si tu veux le mode "pro++".
# Je peux te plug un walk-forward splitter ou une validation croisée si tu veux aller plus loin.

if __name__ == "__main__":
    print("Module de validation prêt à être utilisé dans le pipeline V4.")
