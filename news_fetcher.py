import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title, get_stock_price
from datetime import datetime

def fetch_news_groww():
    url = "https://groww.in/market-news/stocks"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for a in soup.select("a[href^='/market-news/stocks/']"):
        title = a.text.strip()
        href = a['href']
        full_link = "https://groww.in" + href
        if title and full_link:
            articles.append((title, full_link))
    return articles

def get_top_3_stocks():
    headlines = []

    try:
        headlines += fetch_news_groww()
    except Exception as e:
        print("Groww error:", e)

    if not headlines:
        return "❗ No Groww stock news articles found."

    all_news = []
    for title, link in headlines:
        score = analyze_sentiment(title)
        all_news.append((score, title, link))

    top6 = sorted(all_news, reverse=True)[:6]

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

        message += (
            f"{i}️⃣ *{title}*\n"
            f"🔗 [Read more]({link})\n"
            f"{price_info}"
            f"📈 Sentiment Score: {score:.2f}\n\n"
        )

    return message
