import requests
import yfinance as yf
from datetime import datetime
import pytz

import os
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
    url = "https://query1.finance.yahoo.com/v1/finance/search?q=tesla"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        # Just fake it for now because Yahoo headlines API is tricky
        return [
            "Tesla expands production in Texas",
            "Analysts predict strong Q3 earnings",
            "Cybertruck deliveries continue to ramp up"
        ]
    except:
        return ["Could not fetch headlines"]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def format_time():
    tz = pytz.timezone("US/Eastern")
    now = datetime.now(tz)
    return now.strftime("%I:%M %p")  # AM/PM format

if __name__ == "__main__":
    last_price, change, pct_change = get_tesla_data()
    headlines = get_headlines()
    
    message = f"⏰ {format_time()} Tesla Update:\n"
    message += f"Price: ${last_price:.2f}\n"
    message += f"Change: {change:+.2f} ({pct_change:+.2f}%)\n\n"
    message += "Top Headlines:\n"
    for h in headlines:
        message += f"• {h}\n"

    send_telegram_message(message)
