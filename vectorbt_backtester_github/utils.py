# utils.py

import pandas as pd

def compute_rsi(price, period=14):
    """
    Calcule le RSI sur la série de prix.
    """
    delta = price.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)

    avg_gain = up.rolling(period).mean()
    avg_loss = down.rolling(period).mean()

    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def print_separator(title=None):
    """
    Affiche une ligne de séparation stylée (console).
    """
    print("\n" + "="*50)
    if title:
        print(f"=   {title}")
        print("="*50)

def safe_divide(a, b):
    """
    Division protégée (évite division par zéro).
    """
    return a / b if b != 0 else 0

# D'autres utilitaires à rajouter selon besoins
