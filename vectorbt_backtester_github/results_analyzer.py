# results_analyzer.py
# results_analyzer.py - V4 PRO (context-aware)

import os
import pandas as pd
import config

def safe_df(df, fallback=0):
    """Remplace tous les NaN du DataFrame par fallback."""
    return df.fillna(fallback)

def analyze_and_export(results_df):
    """
    Analyse les résultats des backtests, trie et exporte les meilleurs et pires setups,
    robustes (20+ trades, cagr/max_dd valides), pour CHAQUE contexte (uptrend, downtrend, range).
    Gère l'affichage/exports contextuels et prépare le pipeline pour validation OOS.
    """
    if results_df.empty:
        print("Aucun résultat à analyser.")
        return

    # Si la colonne 'context' existe, split par contexte
    if "context" in results_df.columns:
        unique_contexts = results_df["context"].unique()
    else:
        unique_contexts = [None]  # Cas fallback (no context split)

    # Création du dossier results si absent
    os.makedirs(config.RESULTS_DIR, exist_ok=True)

    for ctx in unique_contexts:
        if ctx is not None:
            df_ctx = results_df[results_df["context"] == ctx]
            ctx_str = f"context_{ctx}"
            print(f"\n=== CONTEXTE {ctx} ===")
        else:
            df_ctx = results_df
            ctx_str = "global"
            print("\n=== GLOBAL ===")

        # Filtrage des setups robustes
        filtered = df_ctx[
            (df_ctx["trades"] >= 20) &
            df_ctx["cagr"].notna() & df_ctx["max_dd"].notna()
        ]
        if filtered.empty:
            print("Aucun setup robuste (20+ trades, cagr/max_dd valides).")
            # Afficher et exporter quand même les 5 meilleurs setups bruts (sur le PF)
            best_raw = df_ctx.sort_values(by="pf", ascending=False)
            worst_raw = df_ctx.sort_values(by="pf", ascending=True)
            print("\n=== MEILLEURS SETUPS (bruts, non robustes) ===")
            print(safe_df(best_raw.head(5)[["ma_short", "ma_long", "rsi", "sl_pct", "tp_pct", "trades", "cagr", "sharpe", "max_dd", "pf"]]))
            print("\n=== PIRES SETUPS (bruts, non robustes) ===")
            print(safe_df(worst_raw.head(5)[["ma_short", "ma_long", "rsi", "sl_pct", "tp_pct", "trades", "cagr", "sharpe", "max_dd", "pf"]]))
            # Export CSV aussi
            safe_df(best_raw.head(10)).to_csv(f"{config.RESULTS_DIR}/best_strategies_raw_{ctx_str}.csv", index=False)
            safe_df(worst_raw.head(10)).to_csv(f"{config.RESULTS_DIR}/worst_strategies_raw_{ctx_str}.csv", index=False)
            continue

        # Trier par profit factor décroissant
        best = filtered.sort_values(by="pf", ascending=False)
        worst = filtered.sort_values(by="pf", ascending=True)

        # Exporter les 10 meilleurs et 10 pires setups pour chaque contexte
        safe_df(best.head(10)).to_csv(f"{config.RESULTS_DIR}/best_strategies_{ctx_str}.csv", index=False)
        safe_df(worst.head(10)).to_csv(f"{config.RESULTS_DIR}/worst_strategies_{ctx_str}.csv", index=False)

        # Affichage console
        print("\n=== MEILLEURS SETUPS (robustes) ===")
        print(safe_df(best.head(5)[["ma_short", "ma_long", "rsi", "sl_pct", "tp_pct", "trades", "cagr", "sharpe", "max_dd", "pf"]]))

        print("\n=== PIRES SETUPS (robustes) ===")
        print(safe_df(worst.head(5)[["ma_short", "ma_long", "rsi", "sl_pct", "tp_pct", "trades", "cagr", "sharpe", "max_dd", "pf"]]))

        print(f"\nRésultats exportés dans le dossier : {config.RESULTS_DIR}/")

    print("\n=== SYNTHÈSE FINIE : rapport par contexte ===")

# Plug possible : ajouter affichage colonne 'robust' ou 'robust_ratio' si validator.py est utilisé.
