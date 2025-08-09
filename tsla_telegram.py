import os
import yfinance as yf
import requests
from datetime import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    r.raise_for_status()

def build_message():
    tsla = yf.Ticker("TSLA")
    daily = tsla.history(period="5d")
    y_close = float(daily["Close"].iloc[-2])
    intraday = tsla.history(period="1d", interval="1m")
    last_price = float(intraday["Close"].iloc[-1]) if not intraday.empty else float(daily["Close"].iloc[-1])
    change = last_price - y_close
    pct = (change / y_close) * 100 if y_close else 0.0
    arrow = "📈" if change >= 0 else "📉"

    headlines = []
    try:
        for a in (tsla.news or [])[:3]:
            t = a.get("title", "").strip()
            if t:
                headlines.append(f"📰 {t}")
    except Exception:
        pass

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = [
        f"{arrow} TSLA: ${last_price:,.2f} ({change:+.2f}, {pct:+.2f}%)",
        f"Time: {ts} ET",
        ""
    ] + headlines
    return "\n".join(parts).strip()

if __name__ == "__main__":
    send(build_message())
