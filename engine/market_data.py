import yfinance as yf, pandas as pd

def download_prices(tickers, period='2y'):
    data=yf.download(tickers,period=period,interval='1d',auto_adjust=True,progress=False,group_by='column',threads=True)
    if data.empty: raise RuntimeError('No market data returned')
    close=data['Close'] if isinstance(data.columns,pd.MultiIndex) else data[['Close']]
    if isinstance(close,pd.Series): close=close.to_frame(tickers[0])
    close=close.dropna(axis=1,how='all').sort_index()
    return close
