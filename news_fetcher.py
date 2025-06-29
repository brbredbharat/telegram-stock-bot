import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title
from datetime import datetime

def fetch_groww_stock_news():
    url = "https://groww.in/market-news/stocks"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
    except Exception as e:
        print("Error while fetching Groww stock news:", e)
        return []

    articles = []
    seen = set()
    for a in soup.select("a[href^='/market-news/stocks/']"):
        title = a.get_text(strip=True)
        link = a.get("href")
        if title and link and title not in seen:
            seen.add(title)
            full_link = f"https://groww.in{link}"
            articles.append((title, full_link))
    return articles

def get_prices_for_symbols(symbols):
    if not symbols:
        return {}
    unique = list(set(symbols))
    param = ",".join(f"NSE_{s}" for s in unique)
    url = f"https://api.groww.in/v1/live-data/ltp?segment=CASH&exchange_symbols={param}"
    headers = {"Accept": "application/json"}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        return res.json().get("payload") or {}
    except Exception as e:
        print("Price fetch error:", e)
        return {}

def get_top_3_stocks():
    headlines = fetch_groww_stock_news()
    if not headlines:
        return "❗ No stock news articles found from Groww."

    scored = []
    symbols = []
    for title, link in headlines:
        score = analyze_sentiment(title)
        sym = guess_symbol_from_title(title)
        if sym:
            symbols.append(sym)
        scored.append((score, title, link, sym))

    top6 = sorted(scored, reverse=True)[:6]
    price_map = get_prices_for_symbols([s for (_, _, _, s) in top6 if s])

    message = f"📊 *Top Stock Suggestions ({datetime.now():%Y-%m-%d})*\n\n"
    for idx, (score, title, link, sym) in enumerate(top6, 1):
        price_info = ""
        if sym:
            key = f"NSE_{sym}"
            val = price_map.get(key)
            if val is not None:
                price_info = f"💸 Price: ₹{val}\n"

        message += (
            f"{idx}️⃣ *{title}*\n"
            f"🔗 [Read more]({link})\n"
            f"{price_info}"
            f"📈 Sentiment Score: {score:.2f}\n\n"
        )
    return message
