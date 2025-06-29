import requests
from bs4 import BeautifulSoup
from sentiment import analyze_sentiment
from stock_utils import guess_symbol_from_title, get_stock_info
from datetime import datetime

GOOD_KEYWORDS = [
    "buy", "order", "dividend", "surge", "rises", "jumps", "rallies", "acquire",
    "approval", "stake", "deal", "expansion", "profit", "beats", "soars",
    "raises", "bags", "growth", "upgraded", "recommend", "strong", "positive"
]

def fetch_moneycontrol_buzzing():
    url = "https://www.moneycontrol.com/news/tags/buzzing-stocks.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    articles = []
    seen = set()

    for a in soup.select("ul > li.clearfix > a"):
        title = a.get("title") or a.get_text(strip=True)
        link = a.get("href")

        if not title or not link:
            continue
        if title in seen or "video" in link:
            continue

        full_link = link if link.startswith("http") else f"https://www.moneycontrol.com{link}"
        articles.append((title.strip(), full_link))
        seen.add(title)

        if len(articles) >= 30:
            break

    return articles

def get_top_10_news():
    headlines = fetch_moneycontrol_buzzing()
    if not headlines:
        return "❗ No news found on Moneycontrol buzzing stocks."

    scored = []
    for title, link in headlines:
        title_lower = title.lower()
        if not any(kw in title_lower for kw in GOOD_KEYWORDS):
            continue

        score = analyze_sentiment(title)
        scored.append((score, title, link))

    if not scored:
        return "❗ No strong stock suggestions found from Moneycontrol today."

    top_articles = sorted(scored, reverse=True)[:10]

    message = f"📊 *Top Stock Suggestions ({datetime.now().date()})*\n\n"

    for idx, (score, title, link) in enumerate(top_articles, 1):
        symbol = guess_symbol_from_title(title)
        stock_info = get_stock_info(symbol) if symbol else None

        if stock_info:
            name = stock_info["name"]
            ltp = stock_info["ltp"]
            change = stock_info["changePercent"]
            arrow = "↑" if change >= 0 else "↓"
            message += f"{idx}️⃣ **{name}** at ₹{ltp:.2f} ({arrow} {change:+.2f}%)\n"
        else:
            message += f"{idx}️⃣ {title}\n"

        message += f"🔗 [Read more]({link})\n📈 Sentiment Score: {score:.2f}\n\n"

    return message
