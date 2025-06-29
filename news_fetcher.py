import requests
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title, get_stock_price
from datetime import datetime

def fetch_news_from_stock_feed():
    url = "https://groww.in/v1/api/stories/listing/category/stock_feed?category_type=NEWS&count=20"
    res = requests.get(url)
    data = res.json()
    articles = []

    for item in data.get("data", []):
        title = item.get("story_title", "").strip()
        slug = item.get("slug", "")
        if title and slug:
            full_link = f"https://groww.in/stories/{slug}"
            articles.append((title, full_link))
    return articles

def get_top_3_stocks():
    try:
        headlines = fetch_news_from_stock_feed()
    except Exception as e:
        print("Groww Stock Feed error:", e)
        return "❗ Error while fetching news from Groww."

    if not headlines:
        return "❗ No stock news articles found from Groww feed."

    # Analyze and sort by sentiment
    scored_news = []
    for title, link in headlines:
        score = analyze_sentiment(title)
        scored_news.append((score, title, link))

    # Top 6 by sentiment
    top6 = sorted(scored_news, reverse=True)[:6]

    # Build Telegram-formatted message
    message = f"📊 *Top Stock Suggestions ({datetime.now().strftime('%Y-%m-%d')})*\n\n"

    for i, (score, title, link) in enumerate(top6, 1):
        number = f"{i}️⃣"
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
            f"{number} *{title}*\n"
            f"🔗 [Read more]({link})\n"
            f"{price_info}"
            f"📈 Sentiment Score: {score:.2f}\n\n"
        )

    return message
