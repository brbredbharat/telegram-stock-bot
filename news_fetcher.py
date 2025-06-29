import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sentiment import analyze_sentiment

def get_today_and_yesterday():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    return today, yesterday

def fetch_news_google():
    url = "https://news.google.com/search?q=Indian+stock+market&hl=en-IN&gl=IN&ceid=IN:en"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.select("article h3 a")
    today, yesterday = get_today_and_yesterday()
    results = []

    for article in articles[:20]:
        title = article.text
        href = "https://news.google.com" + article['href'][1:]
        results.append((title, href))

    return results

def get_top_3_stocks():
    headlines = fetch_news_google()
    scored = []

    for title, link in headlines:
        score = analyze_sentiment(title)
        scored.append((score, title, link))

    top3 = sorted(scored, reverse=True)[:3]
    if not top3:
        return "No stock suggestions found for today."

    message = f"📊 *Top Stock Suggestions ({datetime.now().date()})*\n\n"
    for i, (score, title, link) in enumerate(top3, 1):
        message += f"{i}️⃣ {title}\n🔗 [Read more]({link})\n📈 Sentiment Score: {score:.2f}\n\n"

    return message
