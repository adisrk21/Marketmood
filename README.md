# India Market Mood

A deployable Nifty 500 market-breadth dashboard with Market Mood, short/long-term scores, 21/50/200 DMA breadth, RSI breadth, 52-week highs/lows, daily breadth table, historical charts and Telegram regime alerts.

## Data
- Universe: Nifty 500 constituents downloaded at runtime.
- Price history: Yahoo Finance via `yfinance` (`.NS` symbols).
- This is an analytics prototype; validate source/licensing/reliability before commercial use.

## Local run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/backfill.py
streamlit run app.py
```

## GitHub
Create an empty GitHub repository, then from this folder:
```bash
git init
git add .
git commit -m "Initial India Market Mood V1"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/market-mood-india.git
git push -u origin main
```

## Render deployment
1. In Render choose **New > Blueprint** and connect the GitHub repository.
2. Render reads `render.yaml` and creates the Streamlit web service, Postgres database and weekday cron job.
3. Enter `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` when prompted. Never commit these secrets.
4. After deploy, open the web service and click **Refresh market data** once, OR open the cron service and trigger it manually.
5. For full historical backfill, temporarily set the cron Start Command to `python scripts/backfill.py`, trigger once, then restore `python scripts/daily_update.py`; alternatively run backfill locally against the Render external DB URL.

### Schedule
`10 10 * * 1-5` is 10:10 UTC = 15:40 IST, Monday-Friday. It stores the final daily snapshot and sends Telegram only when the regime changes.

## Scoring
Short-term score:
- 35% above 21 DMA
- 20% above 50 DMA
- 20% advance/decline breadth
- 15% RSI breadth
- 10% 52-week high/low breadth

Long-term score:
- 45% above 200 DMA
- 25% above 50 DMA
- 15% 52-week high/low breadth
- 5% RSI breadth
- 10% advance/decline breadth

Market Mood = 60% short-term + 40% long-term.

Regimes: Extreme Bear <20, Bear <35, Weak <45, Neutral <55, Bull <70, Strong Bull <85, Euphoric >=85.

## Notes
- Render cron schedules use UTC.
- Render web services must bind to `0.0.0.0` and `$PORT`.
- PostgreSQL is used in deployment so history survives web-service restarts/redeploys.
