# context.py

import pandas as pd

def detect_trend(price, ma_period=200):
    """
    Retourne une série 'trend' avec les labels :
        1 = uptrend (haussier)
        -1 = downtrend (baissier)
        0 = range (neutre)
    Basé sur la position du prix vs MA200 et la pente de la MA200.
    """
    ma = price.rolling(ma_period).mean()
    # On regarde la pente sur 10 périodes (tu peux adapter)
    ma_slope = ma.diff(10)

    uptrend = (price > ma) & (ma_slope > 0)
    downtrend = (price < ma) & (ma_slope < 0)
    neutral = ~(uptrend | downtrend)

    trend = pd.Series(0, index=price.index)
    trend[uptrend] = 1
    trend[downtrend] = -1
    # neutral est déjà 0

    return trend  # Série Pandas alignée sur le price, 1 / 0 / -1

# Tu pourras étendre pour du multi-timeframe ou d’autres logiques plus tard.
