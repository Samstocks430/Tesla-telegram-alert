import os
import yfinance as yf
import requests
from datetime import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send(msg: str) -> None:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    r.raise_for_status()

def build_message() -> str:
    tsla = yf.Ticker("TSLA")
    daily = tsla.history(period="5d")
    y_close = float(daily["Close"].iloc[-2])

    intraday = tsla.history(period="1d", interval="1m")
    if intraday is not None and not intraday.empty:
        last_price = float(intraday["Close"].iloc[-1])
    else:
        last_price = float(daily["Close"].iloc[-1])

    change = last_price - y_close
    pct = (change / y_close) * 100 if y_close else 0.0
    arrow = "📈" if change >= 0 else "📉"

    headlines = []
    try:
        news = tsla.news or []
        for a in news[:3]:
            title = a.get("title", "").strip()
            if title:
                headlines.append(f"📰 {title}")
    except Exception:
        pass

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = [
        f"{arrow} TSLA: ${last_price:,.2f} ({change:+.2f}, {pct:+.2f}%)",
        f"Time: {ts} ET",
    ]
    if headlines:
        parts.append("")
        parts.extend(headlines)

    return "\n".join(parts)

if __name__ == "__main__":
    send(build_message())
