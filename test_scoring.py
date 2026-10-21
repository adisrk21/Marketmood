from engine.scoring import scores
def test_score_range():
 m=dict(pct_above_21=60,pct_above_50=65,pct_above_200=70,advancers=300,decliners=200,rsi_overbought=60,rsi_oversold=20,high52=30,low52=10)
 st,lt,mo,r=scores(m); assert 0<=st<=100 and 0<=lt<=100 and 0<=mo<=100 and isinstance(r,str)
