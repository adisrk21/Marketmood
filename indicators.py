import numpy as np, pandas as pd

def rsi(s, period=14):
    d=s.diff(); gain=d.clip(lower=0); loss=-d.clip(upper=0)
    ag=gain.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    al=loss.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    rs=ag/al.replace(0,np.nan)
    out=100-(100/(1+rs))
    return out.fillna(100).where(al.ne(0),100)

def add_indicators(close):
    return {
      'close': close, 'ret': close.pct_change()*100,
      'sma21': close.rolling(21).mean(), 'sma50': close.rolling(50).mean(),
      'sma200': close.rolling(200).mean(), 'rsi': rsi(close),
      'high252': close.rolling(252,min_periods=200).max(),
      'low252': close.rolling(252,min_periods=200).min()
    }
