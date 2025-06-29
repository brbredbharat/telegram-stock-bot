import requests
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title
from datetime import datetime

# Groww stock feed API
def fetch_news_from_stock_feed():
    url = "https://groww.in/v1/api/stories/listing/category/stock_feed?category_type=NEWS&count=20"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print("Groww Stock Feed fetch error:", e)
        return []
    articles = []
    for item in data.get("data", []):
        title = item.get("story_title", "").strip()
        slug = item.get("slug", "")
        if title and slug:
            link = f"https://groww.in/stories/{slug}"
            articles.append((title, link))
    return articles

# Public LTP endpoint: https://api.groww.in/v1/live-data/ltp?segment=CASH&exchange_symbols=NSE_RELIANCE
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
        print("Groww LTP fetch error:", e)
        return {}

def get_top_6_stocks():
    headlines = fetch_news_from_stock_feed()
    if not headlines:
        return "❗ No stock news articles found from Groww."

    scored = []
    symbols = []
    for title, link in headlines:
        score = analyze_sentiment(title)
        sym = guess_symbol_from_title(title)
        symbols.append(sym) if sym else None
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
                price = val
                # No direct %; fallback to sentiment only
                price_info = f"💸 Price: ₹{price}\n"
        message += (
            f"{idx}️⃣ *{title}*\n"
            f"🔗 [Read more]({link})\n"
            f"{price_info}"
            f"📈 Sentiment Score: {score:.2f}\n\n"
        )
    return message
