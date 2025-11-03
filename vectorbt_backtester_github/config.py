# config.py

# === PARAMÈTRES GÉNÉRAUX ===
TICKER = "RXL.PA"             # Ticker Yahoo Finance ou autre source
START_DATE = "2016-01-01"     # Date de début du backtest
END_DATE = "2025-07-20"       # Date de fin du backtest
TIMEFRAME = "1d"              # '1d' = daily, '1h' = hourly, etc.

# === PARAMÈTRES STRATÉGIES ===
# Plages élargies pour grid search ou pour générer >10 000 setups
MA_SHORT_RANGE = list(range(10, 61, 5))     # 10, 15, ..., 60 (11 valeurs)
MA_LONG_RANGE  = list(range(80, 241, 20))   # 80, 100, ..., 240 (9 valeurs)
RSI_RANGE      = list(range(20, 51, 5))     # 20, 25, ..., 50 (7 valeurs)
SL_PCT         = [0.01, 0.015, 0.02, 0.025, 0.03]    # 5 valeurs
TP_PCT         = [0.02, 0.03, 0.04, 0.05]            # 4 valeurs

# (Pour les stratégies spéciales type triple MA ou VWMA, ajouter des plages dédiées ici au besoin)

# === AUTRES OPTIONS ===
MIN_TRADES_PER_SETUP = 10
RESULTS_DIR = "results"                # Dossier où sont stockés les résultats CSV

# Tu pourras rajouter ici : liste d'actifs, sélection dynamique, etc.
