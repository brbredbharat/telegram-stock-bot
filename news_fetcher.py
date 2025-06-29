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

    seen = set()
    articles = []
    for item in soup.select("a.buzzing_li"):
        title = item.get_text(strip=True)
        href = item.get("href")
        if title and href and title not in seen:
            seen.add(title)
            link = href if href.startswith("http") else f"https://www.moneycontrol.com{href}"
            articles.append((title, link))
    return articles

def get_top_news():
    headlines = fetch_moneycontrol_buzzing()[:10]
    if not headlines:
        return "❗ No news found on Moneycontrol buzzing stocks."

    message = f"📊 *Top Stock Suggestions ({datetime.now():%Y-%m-%d})*\n\n"
    for idx, (title, link) in enumerate(headlines, 1):
        score = analyze_sentiment(title)
        sym = guess_symbol_from_title(title)
        stock_info = get_stock_info(sym) if sym else None

        if stock_info:
            name = stock_info["name"]
            price = stock_info["ltp"]
            change = stock_info["changePercent"]
            arrow = "↑" if change >= 0 else "↓"
            message += (
                f"{idx}️⃣ {name} at ₹{price:.2f} ({arrow} {change:+.2f}%)\n"
            )
        else:
            message += f"{idx}️⃣ *{title}*\n"

        message += (
            f"🔗 Read more → {link}\n"
            f"📈 Sentiment Score: {score:.2f}\n\n"
        )
    return message
