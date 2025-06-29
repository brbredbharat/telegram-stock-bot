import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title
from datetime import datetime

# List of trusted financial domains
ALLOWED_SOURCES = [
    "moneycontrol.com", "zeebiz.com", "livemint.com", "financialexpress.com",
    "cnbctv18.com", "thehindubusinessline.com", "economictimes.indiatimes.com",
    "business-standard.com", "news18.com", "ndtv.com", "reuters.com", "bqprime.com"
]

# Positive signal keywords for filtering good stock news
GOOD_KEYWORDS = [
    "order", "buy", "acquire", "approval", "dividend", "deal", "record date",
    "invest", "investment", "partner", "partnership", "raises stake", "expansion",
    "license", "contract", "bags order", "growth", "increase", "launch", "revenue up"
]

def fetch_google_financial_news():
    url = "https://news.google.com/search?q=stock+site:moneycontrol.com+OR+site:zeebiz.com+OR+site:livemint.com+OR+site:financialexpress.com+OR+site:cnbctv18.com+OR+site:thehindubusinessline.com+OR+site:economictimes.indiatimes.com+OR+site:business-standard.com+OR+site:news18.com+OR+site:ndtv.com&hl=en-IN&gl=IN&ceid=IN:en"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
    except Exception as e:
        print("Google News fetch error:", e)
        return []

    articles = []
    for a in soup.select("article h3 a"):
        title = a.get_text(strip=True)
        link = a.get("href")
        full_link = "https://news.google.com" + link[1:] if link.startswith(".") else link
        if any(domain in full_link for domain in ALLOWED_SOURCES):
            if any(keyword in title.lower() for keyword in GOOD_KEYWORDS):
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
    headlines = fetch_google_financial_news()
    if not headlines:
        return "❗ No strong stock suggestions found from recent, high-quality news."

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
