import requests
import yfinance as yf
from datetime import datetime
import pytz
import os
import feedparser

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def get_tesla_data():
    tsla = yf.Ticker("TSLA")
    todays_data = tsla.history(period='1d')
    last_price = todays_data['Close'].iloc[-1]
    prev_close = todays_data['Close'].iloc[0]
    change = last_price - prev_close
    pct_change = (change / prev_close) * 100
    return last_price, change, pct_change

def get_headlines():
    rss_url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=TSLA&region=US&lang=en-US"
    try:
        feed = feedparser.parse(rss_url)
        headlines = [entry.title for entry in feed.entries[:3]]
        return headlines if headlines else ["No headlines found"]
    except:
        return ["Could not fetch headlines"]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    last_price, change, pct_change = get_tesla_data()
    headlines = get_headlines()

    # Get time in AM/PM format US Eastern
    eastern = pytz.timezone("US/Eastern")
    now = datetime.now(eastern)
    time_str = now.strftime("%I:%M %p").lstrip("0")

    message = f"{time_str} Tesla Update:\nPrice: ${last_price:.2f}\nChange: {change:+.2f} ({pct_change:+.2f}%)\n\nTop Headlines:"
    for hl in headlines:
        message += f"\n• {hl}"

    send_telegram_message(message)
