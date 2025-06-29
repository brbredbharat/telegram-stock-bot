import requests
from sentiment import analyze_sentiment
from datetime import datetime, timedelta
import yfinance as yf

API_KEY = "pub_a6b9f0105fc5489ab10f6eb0f5c2314f"

# Keywords that suggest positive stock news
GOOD_KEYWORDS = [
    "order", "buy", "dividend", "approval", "growth", "profit", "expansion",
    "acquisition", "revenue", "contract", "record", "strong", "deal"
]

def get_stock_info(stock_name):
    try:
        ticker = yf.Ticker(stock_name + ".NS")  # NSE tickers
        data = ticker.history(period="1d")
        if data.empty:
            return "N/A", "N/A"
        latest = data.iloc[-1]
        price = round(latest["Close"], 2)
        prev_close = round(latest["Open"], 2)
        change_percent = round(((price - prev_close) / prev_close) * 100, 2)
        return f"₹{price}", f"{change_percent:+.2f}%"
    except Exception:
        return "N/A", "N/A"

def fetch_news_from_newsdata():
    today = datetime.utcnow()
    start_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
    url = (
        f"https://newsdata.io/api/1/news?apikey={API_KEY}"
        f"&q=stock&language=en&country=in&from_date={start_date}"
        f"&category=business"
    )

    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching from NewsData.io:", response.text)
        return []

    articles = []
    data = response.json()
    for article in data.get("results", []):
        title = article["title"]
        link = article["link"]
        published = article["pubDate"]

        if any(word in title.lower() for word in GOOD_KEYWORDS):
            score = analyze_sentiment(title)
            articles.append((score, title, link, published))
    return sorted(articles, reverse=True)[:10]

def extract_stock_name(title):
    # Try to find likely stock name from title
    words = title.split()
    for word in words:
        if word.isupper() and len(word) > 2:
            return word
    return words[0]  # fallback

def get_top_news():
    try:
        articles = fetch_news_from_newsdata()
        if not articles:
            return "❗ No strong stock suggestions found from recent NewsData.io headlines."

        message = f"📊 *Top Stock Suggestions ({datetime.now().date()})*\n\n"
        for i, (score, title, link, published) in enumerate(articles, 1):
            stock_name = extract_stock_name(title)
            price, change = get_stock_info(stock_name)
            message += (
                f"{i}️⃣ *{stock_name}* — {title}\n"
                f"💰 Price: {price} | Change: {change}\n"
                f"🔗 [Read more]({link})\n"
                f"📈 Sentiment Score: {score:.2f}\n\n"
            )
        return message
    except Exception as e:
        print("Error in get_top_news:", e)
        return "❗ Something went wrong while fetching stock suggestions."
