import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title, get_stock_price
from datetime import datetime, timedelta
import dateparser

def fetch_news_google():
    url = "https://news.google.com/search?q=Indian+stock+market&hl=en-IN&gl=IN&ceid=IN:en"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for item in soup.select("article"):
        a_tag = item.select_one("h3 a")
        time_tag = item.select_one("time")
        if not a_tag or not time_tag:
            continue

        title = a_tag.text.strip()
        link = a_tag['href']
        full_link = "https://news.google.com" + link[1:] if link.startswith('.') else link
        date_str = time_tag.get("datetime", "")
        pub_date = dateparser.parse(date_str)

        if pub_date and is_recent(pub_date):
            if "stock" in title.lower():
                articles.append((title, full_link, pub_date.date()))
    return articles

def fetch_news_groww():
    url = "https://groww.in/news"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for a in soup.select("a[data-content-id]"):
        title = a.text.strip()
        link = "https://groww.in" + a['href']
        if "stock" not in title.lower():
            continue

        # Groww doesn’t give clear publish date, accept blindly but log for review
        articles.append((title, link, datetime.today().date()))
    return articles

def fetch_news_moneycontrol():
    url = "https://www.moneycontrol.com/news/business/stocks/"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for item in soup.select("li.clearfix"):
        a_tag = item.select_one("a")
        time_tag = item.select_one("span > span")
        if not a_tag:
            continue

        title = a_tag.text.strip()
        link = a_tag['href']
        date_text = time_tag.text.strip() if time_tag else ""

        pub_date = dateparser.parse(date_text)
        if pub_date and is_recent(pub_date):
            if "stock" in title.lower():
                articles.append((title, link, pub_date.date()))
    return articles

def is_recent(pub_date):
    today = datetime.today().date()
    allowed_dates = {today, today - timedelta(days=1), today - timedelta(days=2)}
    return pub_date.date() in allowed_dates

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

    positive_keywords = ["order", "buy", "dividend", "approval", "contract", "revenue", "acquire", "funding", "expansion", "partnership"]
    bad_keywords = [
        "sensex", "nifty", "bse", "market update", "index", "intraday",
        "volume buzz", "pre-market", "closing bell", "f&o", "mutual fund",
        "commodity", "gold", "forex", "today's trading"
    ]

    scored = []
    for title, link, date in headlines:
        title_lower = title.lower()
        if any(bad in title_lower for bad in bad_keywords):
            continue
        if not any(good in title_lower for good in positive_keywords):
            continue

        score = analyze_sentiment(title)
        if score < 0.05:
            continue

        scored.append((score, title, link))

    top6 = sorted(scored, reverse=True)[:6]

    if not top6:
        return "❗ No strong stock suggestions found from recent, high-quality news."

    message = f"📊 *Top Stock Suggestions ({datetime.now().date()})*\n\n"
    for i, (score, title, link) in enumerate(top6, 1):
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
