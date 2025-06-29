import requests
from datetime import datetime, timedelta
import yfinance as yf
from sentiment import analyze_sentiment

API_KEY = "pub_a6b9f0105fc5489ab10f6eb0f5c2314f"

def get_stock_info(stock_name):
    try:
        ticker = yf.Ticker(stock_name + ".NS")
        data = ticker.history(period="1d")
        if data.empty:
            return "N/A", "N/A"
        latest = data.iloc[-1]
        price = round(latest["Close"], 2)
        prev = round(latest["Open"], 2)
        change = round(((price - prev) / prev) * 100, 2)
        return f"₹{price}", f"{change:+.2f}%"
    except:
        return "N/A", "N/A"

def extract_stock_name(title):
    words = title.split()
    for word in words:
        if word.isupper() and len(word) > 2:
            return word
    return words[0]

def fetch_news():
    from_date = (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d")
    url = (
        f"https://newsdata.io/api/1/news?apikey={API_KEY}"
        f"&q=stock&language=en&country=in&category=business&from_date={from_date}"
    )

    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        articles = data.get("results", [])
        return articles[:10]  # Top 10 only
    except Exception as e:
        print("❗ Error fetching NewsData:", e)
        return []

def get_top_news():
    articles = fetch_news()
    if not articles:
        return "❗ Still no stock news articles found from NewsData.io."

    message = f"📊 *Top Stock Suggestions ({datetime.now().date()})*\n\n"
    for i, article in enumerate(articles, 1):
        title = article["title"]
        link = article["link"]
        stock = extract_stock_name(title)
        price, change = get_stock_info(stock)
        score = analyze_sentiment(title)
        message += (
            f"{i}️⃣ *{stock}* — {title}\n"
            f"💰 Price: {price} | Change: {change}\n"
            f"🔗 [Read more]({link})\n"
            f"📈 Sentiment Score: {score:.2f}\n\n"
        )

    return message
