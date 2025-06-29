import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
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

    scored = []
    for title, link in headlines:
        score = analyze_sentiment(title)
        scored.append((score, title, link))

    top3 = sorted(scored, reverse=True)[:3]

    if not top3:
        return "❗ No valid stock news found for today or yesterday."

    message = f"📊 *Top Stock Suggestions ({datetime.now().date()})*\n\n"
    for i, (score, title, link) in enumerate(top3, 1):
        message += f"{i}️⃣ {title}\n🔗 [Read more]({link})\n📈 Sentiment Score: {score:.2f}\n\n"

    return message
