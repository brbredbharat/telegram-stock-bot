import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title, get_stock_price
from datetime import datetime

def fetch_news_google():
    url = "https://news.google.com/search?q=Indian+stock+market&hl=en-IN&gl=IN&ceid=IN:en"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for a in soup.select("article h3 a"):
        title = a.text.strip()
        link = a['href']
        full_link = "https://news.google.com" + link[1:] if link.startswith('.') else link
        if "stock" in title.lower():
            articles.append((title, full_link))
    return articles

def fetch_news_groww():
    url = "https://groww.in/news"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for a in soup.select("a[data-content-id]"):
        title = a.text.strip()
        link = "https://groww.in" + a['href']
        if "stock" in title.lower():
            articles.append((title, link))
    return articles

def fetch_news_moneycontrol():
    url = "https://www.moneycontrol.com/news/business/stocks/"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for a in soup.select("h2 a"):
        title = a.text.strip()
        link = a['href']
        if "stock" in title.lower():
            articles.append((title, link))
    return articles

def get_top_3_stocks():
    headlines = []

    try:
        headlines += fetch_news_google()
    except Exception as e:
        print("Google News error:", e)
    try:
        headlines += fetch_news_groww()
    except Exception as e:
        print("Groww error:", e)
    try:
        headlines += fetch_news_moneycontrol()
    except Exception as e:
        print("Moneycontrol error:", e)

    # ❌ Filter out generic or vague titles
    bad_keywords = [
        "gainers", "losers", "top 10", "top stocks", "sensex", "nifty", "bse", "stock market",
        "today’s trading", "intraday", "market update", "index", "volume buzz", "pre-market", "closing bell"
    ]

    scored = []
    for title, link in headlines:
        title_lower = title.lower()
        if any(bad in title_lower for bad in bad_keywords):
            continue  # Skip generic news

        score = analyze_sentiment(title)
        scored.append((score, title, link))

    # Sort and pick top 3
    top3 = sorted(scored, reverse=True)[:3]

    if not top3:
        return "❗ No valid stock news found for today or yesterday."

    message = f"📊 *Top Stock Suggestions ({datetime.now().date()})*\n\n"
    for i, (score, title, link) in enumerate(top3, 1):
        symbol = guess_symbol_from_title(title)
        if symbol:
            price, change = get_stock_price(symbol)
            if price and change:
                price_info = f"💸 Price: ₹{price} ({change}%)\n"
            else:
                price_info = ""
        else:
            price_info = ""

        message += f"{i}️⃣ {title}\n🔗 [Read more]({link})\n{price_info}📈 Sentiment Score: {score:.2f}\n\n"

    return message
