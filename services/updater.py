from config import DATA_PERIOD
from engine.universe import get_nifty500
from engine.market_data import download_prices
from engine.breadth import build_history
from database.repository import upsert, read_all
from services.telegram import send

def update(backfill=False, notify=False):
    old=read_all(); prev=old.iloc[-1] if len(old) else None
    tickers=get_nifty500(); close=download_prices(tickers,DATA_PERIOD)
    hist=build_history(close)
    if hist.empty: raise RuntimeError('No breadth history calculated')
    save=hist if backfill else hist.tail(5)
    upsert(save)
    latest=hist.iloc[-1]
    if notify and (prev is None or prev['regime']!=latest['regime']):
        msg=(f'INDIA MARKET MOOD\n\nMood: {latest.mood_score:.1f}/100 - {latest.regime}\n'
             f'Short: {latest.short_score:.1f} | Long: {latest.long_score:.1f}\n'
             f'>21DMA {latest.pct_above_21:.1f}% | >50DMA {latest.pct_above_50:.1f}% | >200DMA {latest.pct_above_200:.1f}%\n'
             f'A/D: {latest.ad_ratio:.2f} | 52W H/L: {latest.high52}/{latest.low52}')
        send(msg)
    return latest
