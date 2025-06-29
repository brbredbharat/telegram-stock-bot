import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title, get_stock_price
from datetime import datetime
import dateparser

def fetch_news_google():
    url = "https://news.google.com/search?q=Indian+stock+market&hl=en-IN&gl=IN&ceid=IN:en"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for item in soup.select("article"):
        a_tag = item.select_one("h3 a")
        if not a_tag:
            continue
        title = a_tag.text.strip()
        link = a_tag['href']
        full_link = "https://news.google.com" + link[1:] if link.startswith('.') else link
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
        articles.append((title, link))
    return articles

def fetch_news_moneycontrol():
    url = "https://www.moneycontrol.com/news/business/stocks/"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for item in soup.select("li.clearfix"):
        a_tag = item.select_one("a")
        if not a_tag:
            continue
        title = a_tag.text.strip()
        link = a_tag['href']
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

    if not headlines:
        return "❗ Still no news found from Google, Groww, or Moneycontrol."

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

        message += f"{i}️⃣ {title}\n🔗 [Read more]({link})\n{price_info}📈 Sentiment Score: {score:.2f}\n\n"

    return message
