import pandas as pd, numpy as np
from engine.indicators import rsi
from engine.scoring import scores

def build_history(close):
    sma21=close.rolling(21).mean(); sma50=close.rolling(50).mean(); sma200=close.rolling(200).mean()
    ret=close.pct_change()*100
    delta=close.diff(); gain=delta.clip(lower=0); loss=-delta.clip(upper=0)
    ag=gain.ewm(alpha=1/14,adjust=False,min_periods=14).mean(); al=loss.ewm(alpha=1/14,adjust=False,min_periods=14).mean()
    rs=ag/al.replace(0,np.nan); rsiv=(100-(100/(1+rs))).fillna(100).where(al.ne(0),100)
    hi=close.rolling(252,min_periods=200).max(); lo=close.rolling(252,min_periods=200).min()
    rows=[]
    for d in close.index:
        c=close.loc[d]; valid=c.notna(); n=int(valid.sum())
        if n<20: continue
        rr=ret.loc[d]
        m={'date':pd.Timestamp(d).date(),'total_stocks':n,
           'pct_above_21':100*((c>sma21.loc[d])&valid).sum()/n,
           'pct_above_50':100*((c>sma50.loc[d])&valid).sum()/n,
           'pct_above_200':100*((c>sma200.loc[d])&valid).sum()/n,
           'advancers':int((rr>0).sum()),'decliners':int((rr<0).sum()),
           'up3':int((rr>=3).sum()),'down3':int((rr<=-3).sum()),
           'up5':int((rr>=5).sum()),'down5':int((rr<=-5).sum()),
           'up10':int((rr>=10).sum()),'down10':int((rr<=-10).sum()),
           'up20':int((rr>=20).sum()),'down20':int((rr<=-20).sum()),
           'rsi_overbought':int((rsiv.loc[d]>=70).sum()),'rsi_oversold':int((rsiv.loc[d]<=30).sum()),
           'high52':int((c>=hi.loc[d]*0.999).sum()),'low52':int((c<=lo.loc[d]*1.001).sum())}
        m['ad_ratio']=m['advancers']/max(m['decliners'],1)
        st,lt,mo,reg=scores(m); m.update(short_score=st,long_score=lt,mood_score=mo,regime=reg)
        rows.append(m)
    return pd.DataFrame(rows)
