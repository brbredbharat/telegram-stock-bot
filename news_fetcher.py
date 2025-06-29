import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title, get_stock_info
from datetime import datetime

DOMAINS = [
    "moneycontrol.com", "livemint.com", "financialexpress.com", "zeebiz.com",
    "cnbctv18.com", "thehindubusinessline.com", "economictimes.indiatimes.com",
    "business-standard.com", "news18.com", "ndtv.com", "reuters.com", "bqprime.com"
]

def fetch_google_financial_news():
    query = "+OR+".join([f"site:{d}" for d in DOMAINS])
    url = f"https://news.google.com/search?q=stock+({query})&hl=en-IN&gl=IN&ceid=IN:en"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("article")
    results = []
    for art in items:
        a = art.select_one("h3 a")
        if not a:
            continue
        title = a.get_text(strip=True)
        href = a["href"]
        link = "https://news.google.com" + href[1:]
        if any(d in link for d in DOMAINS):
            results.append((title, link))
        if len(results) >= 12:
            break
    return results

def get_top_news():
    headlines = fetch_google_financial_news()
    scored = []
    for title, link in headlines:
        score = analyze_sentiment(title)
        sym = guess_symbol_from_title(title)
        stock_info = get_stock_info(sym) if sym else None
        scored.append((score, title, link, sym, stock_info))

    top10 = sorted(scored, key=lambda x: x[0], reverse=True)[:10]
    message = f"📊 *Top Stock Suggestions ({datetime.now():%Y-%m-%d})*\n\n"

    for idx, (score, title, link, sym, info) in enumerate(top10, 1):
        if info:
            name = info["name"]
            price = info["ltp"]
            change = info["changePercent"]
            arrow = "↑" if change >= 0 else "↓"
            line = f"{idx}️⃣ {name} at ₹{price:.2f} ({arrow} {change:+.2f}%)\n"
        else:
            line = f"{idx}️⃣ *{title}*\n"
        message += (
            line +
            f"🔗 [Read more]({link})\n" +
            f"📈 Sentiment Score: {score:.2f}\n\n"
        )
    return message
