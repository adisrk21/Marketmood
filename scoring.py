def clamp(x): return max(0.0,min(100.0,float(x)))
def ratio_score(a,b):
    n=a+b
    return 50.0 if n<=0 else 100.0*a/n

def scores(m):
    rsi=ratio_score(m['rsi_overbought'],m['rsi_oversold'])
    hl=ratio_score(m['high52'],m['low52'])
    ad=ratio_score(m['advancers'],m['decliners'])
    st=.35*m['pct_above_21']+.20*m['pct_above_50']+.20*ad+.15*rsi+.10*hl
    lt=.45*m['pct_above_200']+.25*m['pct_above_50']+.15*hl+.05*rsi+.10*ad
    mood=.60*st+.40*lt
    if mood<20:r='EXTREME BEAR'
    elif mood<35:r='BEAR'
    elif mood<45:r='WEAK'
    elif mood<55:r='NEUTRAL'
    elif mood<70:r='BULL'
    elif mood<85:r='STRONG BULL'
    else:r='EUPHORIC'
    return round(clamp(st),1),round(clamp(lt),1),round(clamp(mood),1),r
