import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title, get_stock_info
from datetime import datetime

def fetch_moneycontrol_buzzing():
    url = "https://www.moneycontrol.com/news/tags/buzzing-stocks.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    articles = []
    seen = set()

    # Updated selector to find proper news article links
    for item in soup.select("ul > li.clearfix > a"):
        title = item.get("title") or item.get_text(strip=True)
        link = item.get("href")

        if not title or not link:
            continue

        if title in seen or "video" in link:
            continue

        full_link = link if link.startswith("http") else f"https://www.moneycontrol.com{link}"
        articles.append((title.strip(), full_link))
        seen.add(title)

        if len(articles) >= 20:
            break

    return articles

def get_top_news():
    headlines = fetch_moneycontrol_buzzing()
    if not headlines:
        return "❗ No news found on Moneycontrol buzzing stocks."

    message = f"📊 *Top Stock Suggestions ({datetime.now().date()})*\n\n"
    count = 0

    for idx, (title, link) in enumerate(headlines, 1):
        score = analyze_sentiment(title)
        if score < 0.2:
            continue  # Skip weak headlines

        symbol = guess_symbol_from_title(title)
        stock_info = get_stock_info(symbol) if symbol else None

        if stock_info:
            name = stock_info["name"]
            ltp = stock_info["ltp"]
            change = stock_info["changePercent"]
            arrow = "↑" if change >= 0 else "↓"
            message += f"{idx}️⃣ {name} at ₹{ltp:.2f} ({arrow} {change:+.2f}%)\n"
        else:
            message += f"{idx}️⃣ *{title}*\n"

        message += f"🔗 [Read more]({link})\n📈 Sentiment Score: {score:.2f}\n\n"
        count += 1
        if count >= 10:
            break

    if count == 0:
        return "❗ No strong stock suggestions found from Moneycontrol today."

    return message
