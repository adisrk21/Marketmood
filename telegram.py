import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return False
    u=f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    r=requests.post(u,json={'chat_id':TELEGRAM_CHAT_ID,'text':text},timeout=20); r.raise_for_status(); return True
