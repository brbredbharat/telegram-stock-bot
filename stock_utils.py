import requests
import csv
from io import StringIO

symbol_map = {}

def load_symbol_map():
    global symbol_map
    try:
        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        decoded = response.content.decode("utf-8")
        reader = csv.DictReader(StringIO(decoded))
        for row in reader:
            name = row["Company Name"].strip().lower()
            symbol = row["Symbol"].strip()
            symbol_map[name] = symbol
    except Exception as e:
        print("❗ Error loading NSE symbols:", e)

def guess_symbol_from_title(title):
    title_words = set(title.lower().split())
    best_match = None
    highest_score = 0

    for company_name, symbol in symbol_map.items():
        company_words = set(company_name.lower().split())
        score = len(company_words & title_words) / len(company_words)
        if score > highest_score and score >= 0.6:
            best_match = symbol
            highest_score = score

    return best_match

def get_stock_info(symbol):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}",
        }
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"

        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers, timeout=5)
        res = session.get(url, headers=headers, timeout=5)
        data = res.json()

        name = data["info"]["companyName"]
        ltp = float(data["priceInfo"]["lastPrice"])
        pchange = float(data["priceInfo"]["pChange"])
        arrow = "↑" if pchange >= 0 else "↓"

        return f"**{name}** at ₹{ltp:.2f} ({arrow} {pchange:+.2f}%)"
    except Exception as e:
        print(f"❗ Error fetching price for {symbol}: {e}")
        return None

# Load on import
load_symbol_map()
