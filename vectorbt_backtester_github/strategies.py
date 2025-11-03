# strategies.py

# strategies.py

import numpy as np
import pandas as pd
import config

def generate_setups():
    """
    Génère toutes les combinaisons de setups possibles à tester pour la stratégie 'moving_average_crossover'.
    Chaque setup est un dict avec les paramètres à utiliser.
    """
    setups = []
    for ma_short in config.MA_SHORT_RANGE:
        for ma_long in config.MA_LONG_RANGE:
            if ma_short >= ma_long:
                continue  # On évite les setups incohérents
            for rsi_val in config.RSI_RANGE:
                for sl in config.SL_PCT:
                    for tp in config.TP_PCT:
                        setups.append({
                            "ma_short": ma_short,
                            "ma_long": ma_long,
                            "rsi": rsi_val,
                            "sl_pct": sl,
                            "tp_pct": tp
                        })
    return setups
# Exemple de setup_generator pour une autre stratégie :
# def generate_setups_breakout():
#     setups = []
#     for window in [10, 20, 50]:
#         for sl in [0.01, 0.02]:
#             for tp in [0.03, 0.05]:
#                 setups.append({"window": window, "sl_pct": sl, "tp_pct": tp})
#     return setups

def moving_average_crossover(price, ma_short, ma_long, **kwargs):
    """
    Croisement de moyennes mobiles : entrée quand la MA courte croise au-dessus de la MA longue.
    Sortie sur croisement inverse.
    """
    ma_s = price.rolling(ma_short).mean()
    ma_l = price.rolling(ma_long).mean()
    entries = (ma_s > ma_l) & (ma_s.shift(1) <= ma_l.shift(1))
    exits = (ma_s < ma_l) & (ma_s.shift(1) >= ma_l.shift(1))
    return entries, exits

def rsi_pullback(price, rsi_period, rsi_val, **kwargs):
    """
    RSI Pullback : entrée si RSI < seuil, sortie si RSI > 50.
    """
    import pandas_ta as ta
    rsi = ta.rsi(price, length=rsi_period)
    entries = rsi < rsi_val
    exits = rsi > 50
    return entries, exits

def breakout_high(price, window, **kwargs):
    """
    Breakout : entrée si prix casse le plus haut sur 'window' périodes, sortie si prix repasse sous ce niveau.
    """
    high = price.rolling(window).max()
    entries = price > high.shift(1)
    exits = price < high.shift(1)
    return entries, exits

def breakout_low(price, window, **kwargs):
    """
    Breakout : entrée si prix casse le plus bas sur 'window' périodes, sortie si prix repasse au-dessus.
    """
    low = price.rolling(window).min()
    entries = price < low.shift(1)
    exits = price > low.shift(1)
    return entries, exits

def mean_reversion(price, window, thresh, **kwargs):
    """
    Mean Reversion : entrée si prix s'écarte de la moyenne de 'window' de plus de 'thresh' %, sortie sur retour à la moyenne.
    """
    ma = price.rolling(window).mean()
    dev = (price - ma) / ma
    entries = dev < -thresh
    exits = price > ma
    return entries, exits

def momentum(price, window, thresh, **kwargs):
    """
    Momentum : entrée si rendement sur 'window' périodes > 'thresh', sortie si rendement < 0.
    """
    returns = price.pct_change(window)
    entries = returns > thresh
    exits = returns < 0
    return entries, exits

def macd_cross(price, fast=12, slow=26, signal=9, **kwargs):
    """
    MACD : entrée quand MACD croise au-dessus de son signal, sortie sur croisement inverse.
    """
    ema_fast = price.ewm(span=fast, adjust=False).mean()
    ema_slow = price.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    entries = (macd > macd_signal) & (macd.shift(1) <= macd_signal.shift(1))
    exits = (macd < macd_signal) & (macd.shift(1) >= macd_signal.shift(1))
    return entries, exits

def bollinger_band_break(price, window, n_std, **kwargs):
    """
    Bollinger Bands Break : entrée si prix casse la bande supérieure, sortie si prix repasse sous la moyenne.
    """
    ma = price.rolling(window).mean()
    std = price.rolling(window).std()
    upper = ma + n_std * std
    entries = price > upper
    exits = price < ma
    return entries, exits

def bollinger_mean_revert(price, window, n_std, **kwargs):
    """
    Bollinger Mean Revert : entrée si prix casse la bande inférieure, sortie sur retour à la moyenne.
    """
    ma = price.rolling(window).mean()
    std = price.rolling(window).std()
    lower = ma - n_std * std
    entries = price < lower
    exits = price > ma
    return entries, exits

def support_resistance_break(price, window, **kwargs):
    """
    Support/Resistance : entrée si prix casse la résistance (max sur window), sortie si prix repasse sous la résistance.
    """
    resistance = price.rolling(window).max()
    entries = price > resistance.shift(1)
    exits = price < resistance.shift(1)
    return entries, exits

def range_bound(price, window, **kwargs):
    """
    Range Bound : entrée si prix touche la borne basse (min sur window), sortie si prix touche la borne haute.
    """
    low = price.rolling(window).min()
    high = price.rolling(window).max()
    entries = price <= low
    exits = price >= high
    return entries, exits

def stochastic_cross(price, k_period, d_period, thresh_low=20, thresh_high=80, **kwargs):
    """
    Stochastic Oscillator : entrée si %K croise au-dessus de %D sous thresh_low, sortie si %K croise sous %D au-dessus de thresh_high.
    """
    low = price.rolling(k_period).min()
    high = price.rolling(k_period).max()
    k = 100 * (price - low) / (high - low)
    d = k.rolling(d_period).mean()
    entries = (k > d) & (k.shift(1) <= d.shift(1)) & (k < thresh_low)
    exits = (k < d) & (k.shift(1) >= d.shift(1)) & (k > thresh_high)
    return entries, exits

def donchian_breakout(price, window, **kwargs):
    """
    Donchian Channel Breakout : entrée si prix casse le plus haut/bas du canal, sortie sur retour dans le canal.
    """
    high = price.rolling(window).max()
    low = price.rolling(window).min()
    entries = price > high.shift(1)
    exits = price < low.shift(1)
    return entries, exits

def atr_trailing_stop(price, atr_period, multiplier, **kwargs):
    """
    ATR Trailing Stop : entrée si prix casse au-dessus de la moyenne, sortie si prix casse sous un stop basé sur ATR.
    """
    tr = np.maximum(price.diff(), np.maximum(price - price.shift(1), price.shift(1) - price))
    atr = tr.rolling(atr_period).mean()
    ma = price.rolling(atr_period).mean()
    stop = ma - multiplier * atr
    entries = price > ma
    exits = price < stop
    return entries, exits

def rsi_overbought_oversold(price, rsi_period, overbought=70, oversold=30, **kwargs):
    """
    RSI Overbought/Oversold : entrée si RSI < oversold, sortie si RSI > overbought.
    """
    import pandas_ta as ta
    rsi = ta.rsi(price, length=rsi_period)
    entries = rsi < oversold
    exits = rsi > overbought
    return entries, exits

def ema_crossover(price, ema_fast, ema_slow, **kwargs):
    """
    EMA Crossover : entrée si EMA rapide croise au-dessus de la lente, sortie sur croisement inverse.
    """
    fast = price.ewm(span=ema_fast, adjust=False).mean()
    slow = price.ewm(span=ema_slow, adjust=False).mean()
    entries = (fast > slow) & (fast.shift(1) <= slow.shift(1))
    exits = (fast < slow) & (fast.shift(1) >= slow.shift(1))
    return entries, exits

def parabolic_sar(price, af=0.02, max_af=0.2, **kwargs):
    """
    Parabolic SAR : entrée si prix croise au-dessus du SAR, sortie sur croisement inverse.
    """
    import pandas_ta as ta
    sar = ta.psar(price, af=af, max_af=max_af)["PSARl_0.02_0.2"]
    entries = price > sar
    exits = price < sar
    return entries, exits

def triple_ma_crossover(price, ma1, ma2, ma3, **kwargs):
    """
    Triple MA Crossover : entrée si MA courte > MA moyenne > MA longue, sortie si l'ordre s'inverse.
    """
    m1 = price.rolling(ma1).mean()
    m2 = price.rolling(ma2).mean()
    m3 = price.rolling(ma3).mean()
    entries = (m1 > m2) & (m2 > m3) & ~((m1.shift(1) > m2.shift(1)) & (m2.shift(1) > m3.shift(1)))
    exits = (m1 < m2) & (m2 < m3) & ~((m1.shift(1) < m2.shift(1)) & (m2.shift(1) < m3.shift(1)))
    return entries, exits

def vwma_crossover(price, volume, short, long, **kwargs):
    """
    VWMA Crossover : entrée si VWMA courte croise au-dessus de la VWMA longue, sortie sur croisement inverse.
    """
    vwma_short = (price * volume).rolling(short).sum() / volume.rolling(short).sum()
    vwma_long = (price * volume).rolling(long).sum() / volume.rolling(long).sum()
    entries = (vwma_short > vwma_long) & (vwma_short.shift(1) <= vwma_long.shift(1))
    exits = (vwma_short < vwma_long) & (vwma_short.shift(1) >= vwma_long.shift(1))
    return entries, exits

def price_channel_break(price, window, **kwargs):
    """
    Price Channel Break : entrée si prix casse la borne supérieure du canal, sortie si prix repasse sous la moyenne.
    """
    high = price.rolling(window).max()
    ma = price.rolling(window).mean()
    entries = price > high.shift(1)
    exits = price < ma
    return entries, exits

def supertrend_entry(price, atr_period=10, multiplier=3, **kwargs):
    """
    Supertrend : entrée si prix croise au-dessus du Supertrend, sortie sur croisement inverse.
    """
    import pandas_ta as ta
    st = ta.supertrend(length=atr_period, multiplier=multiplier)["SUPERT_10_3.0"]
    entries = price > st
    exits = price < st
    return entries, exits

def cci_entry(price, cci_period=20, thresh=100, **kwargs):
    """
    CCI : entrée si CCI > thresh, sortie si CCI < 0.
    """
    import pandas_ta as ta
    cci = ta.cci(price, length=cci_period)
    entries = cci > thresh
    exits = cci < 0
    return entries, exits

def adx_trend(price, adx_period=14, thresh=25, **kwargs):
    """
    ADX Trend : entrée si ADX > thresh et +DI > -DI, sortie si ADX < thresh ou -DI > +DI.
    """
    import pandas_ta as ta
    adx = ta.adx(price, length=adx_period)
    entries = (adx["ADX_14"] > thresh) & (adx["DMP_14"] > adx["DMN_14"])
    exits = (adx["ADX_14"] < thresh) | (adx["DMN_14"] > adx["DMP_14"])
    return entries, exits

def turtle_breakout(price, window, **kwargs):
    """
    Turtle Breakout : entrée si prix casse le plus haut sur window, sortie si prix casse le plus bas sur window.
    """
    high = price.rolling(window).max()
    low = price.rolling(window).min()
    entries = price > high.shift(1)
    exits = price < low.shift(1)
    return entries, exits

def heikin_ashi_trend(price, **kwargs):
    """
    Heikin Ashi Trend : entrée si bougie HA verte, sortie si bougie HA rouge.
    """
    import pandas_ta as ta
    ha = ta.ha(open_=price, high=price, low=price, close=price)
    entries = ha["HA_close"] > ha["HA_open"]
    exits = ha["HA_close"] < ha["HA_open"]
    return entries, exits

STRATEGY_FUNCS = {
    "moving_average_crossover": moving_average_crossover,
    "rsi_pullback": rsi_pullback,
    "breakout_high": breakout_high,
    "breakout_low": breakout_low,
    "mean_reversion": mean_reversion,
    "momentum": momentum,
    "macd_cross": macd_cross,
    "bollinger_band_break": bollinger_band_break,
    "bollinger_mean_revert": bollinger_mean_revert,
    "support_resistance_break": support_resistance_break,
    "range_bound": range_bound,
    "stochastic_cross": stochastic_cross,
    "donchian_breakout": donchian_breakout,
    "atr_trailing_stop": atr_trailing_stop,
    "rsi_overbought_oversold": rsi_overbought_oversold,
    "ema_crossover": ema_crossover,
    "parabolic_sar": parabolic_sar,
    "triple_ma_crossover": triple_ma_crossover,
    "vwma_crossover": vwma_crossover,
    "price_channel_break": price_channel_break,
    "supertrend_entry": supertrend_entry,
    "cci_entry": cci_entry,
    "adx_trend": adx_trend,
    "turtle_breakout": turtle_breakout,
    "heikin_ashi_trend": heikin_ashi_trend,
}
