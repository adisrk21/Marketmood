import pandas as pd
from sqlalchemy import text
from database.db import engine, init_db

def upsert(df):
    init_db()
    sql=text('''INSERT INTO market_daily(date,total_stocks,pct_above_21,pct_above_50,pct_above_200,advancers,decliners,ad_ratio,up3,down3,up5,down5,up10,down10,up20,down20,rsi_overbought,rsi_oversold,high52,low52,short_score,long_score,mood_score,regime)
    VALUES(:date,:total_stocks,:pct_above_21,:pct_above_50,:pct_above_200,:advancers,:decliners,:ad_ratio,:up3,:down3,:up5,:down5,:up10,:down10,:up20,:down20,:rsi_overbought,:rsi_oversold,:high52,:low52,:short_score,:long_score,:mood_score,:regime)
    ON CONFLICT(date) DO UPDATE SET total_stocks=excluded.total_stocks,pct_above_21=excluded.pct_above_21,pct_above_50=excluded.pct_above_50,pct_above_200=excluded.pct_above_200,advancers=excluded.advancers,decliners=excluded.decliners,ad_ratio=excluded.ad_ratio,up3=excluded.up3,down3=excluded.down3,up5=excluded.up5,down5=excluded.down5,up10=excluded.up10,down10=excluded.down10,up20=excluded.up20,down20=excluded.down20,rsi_overbought=excluded.rsi_overbought,rsi_oversold=excluded.rsi_oversold,high52=excluded.high52,low52=excluded.low52,short_score=excluded.short_score,long_score=excluded.long_score,mood_score=excluded.mood_score,regime=excluded.regime''')
    with engine.begin() as c:
        for r in df.to_dict('records'): c.execute(sql,r)

def read_all():
    init_db()
    return pd.read_sql('SELECT * FROM market_daily ORDER BY date',engine,parse_dates=['date'])
