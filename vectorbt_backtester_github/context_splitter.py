

"""
context_splitter.py

Module pour taguer chaque période de l'historique avec un contexte de marché (trend, range, etc.).
Permet ensuite de backtester ou valider par contexte.

Usage :
    from context_splitter import split_by_context

    price_data = ... # DataFrame OHLC
    context_labels = split_by_context(price_data)
    # Ajoute une colonne 'context' à price_data : 1 = uptrend, -1 = downtrend, 0 = range

A personnaliser selon tes critères de trend.

"""

import pandas as pd

def split_by_context(price_data, ma_len=200, trend_lookback=10):
    """
    Ajoute une colonne 'context' à price_data :
    - 1 : uptrend (MA200 haussière + prix au-dessus)
    - -1 : downtrend (MA200 baissière + prix en dessous)
    - 0 : range/neutre
    """
    df = price_data.copy()
    ma = df['Close'].rolling(ma_len).mean()
    ma_slope = ma.diff(trend_lookback)
    # Contexte uptrend
    uptrend = (df['Close'] > ma) & (ma_slope > 0)
    # Contexte downtrend
    downtrend = (df['Close'] < ma) & (ma_slope < 0)
    # Range sinon
    context = pd.Series(0, index=df.index)
    context[uptrend] = 1
    context[downtrend] = -1
    df['context'] = context
    return df

if __name__ == "__main__":
    print("Module de split par contexte prêt à être utilisé.")
