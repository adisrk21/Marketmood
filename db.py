from sqlalchemy import create_engine, text
from config import DATABASE_URL

url = DATABASE_URL
if url.startswith('postgres://'):
    url = url.replace('postgres://', 'postgresql+psycopg://', 1)
elif url.startswith('postgresql://'):
    url = url.replace('postgresql://', 'postgresql+psycopg://', 1)
engine = create_engine(url, pool_pre_ping=True)

def init_db():
    ddl = '''
    CREATE TABLE IF NOT EXISTS market_daily (
      date DATE PRIMARY KEY,
      total_stocks INTEGER,
      pct_above_21 REAL, pct_above_50 REAL, pct_above_200 REAL,
      advancers INTEGER, decliners INTEGER, ad_ratio REAL,
      up3 INTEGER, down3 INTEGER, up5 INTEGER, down5 INTEGER,
      up10 INTEGER, down10 INTEGER, up20 INTEGER, down20 INTEGER,
      rsi_overbought INTEGER, rsi_oversold INTEGER,
      high52 INTEGER, low52 INTEGER,
      short_score REAL, long_score REAL, mood_score REAL,
      regime TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );'''
    with engine.begin() as c: c.execute(text(ddl))
