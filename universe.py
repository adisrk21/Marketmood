import io, requests, pandas as pd

URLS = [
 'https://www.niftyindices.com/IndexConstituent/ind_nifty500list.csv',
 'https://archives.nseindia.com/content/indices/ind_nifty500list.csv'
]

def get_nifty500():
    headers={'User-Agent':'Mozilla/5.0'}
    last=None
    for url in URLS:
        try:
            r=requests.get(url,headers=headers,timeout=20); r.raise_for_status()
            df=pd.read_csv(io.StringIO(r.text))
            col=next(c for c in df.columns if c.strip().lower()=='symbol')
            syms=df[col].dropna().astype(str).str.strip().unique().tolist()
            return [s+'.NS' for s in syms]
        except Exception as e: last=e
    raise RuntimeError(f'Unable to download Nifty 500 constituents: {last}')
