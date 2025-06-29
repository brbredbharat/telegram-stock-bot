import requests
import csv
import difflib
from io import StringIO

symbol_map = {}

def load_symbol_map():
    global symbol_map
    try:
        url = "https://www1.nseindia.com/content/equities/EQUITY_L.csv"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        decoded = response.content.decode("utf-8")
        reader = csv.DictReader(StringIO(decoded))
        for row in reader:
            name = row["Company Name"].lower()
            symbol = row["Symbol"]
            symbol_map[name] = symbol
    except Exception as e:
        print("Error loading symbol map:", e)

def guess_symbol_from_title(title):
    title = title.lower()
    best_match = difflib.get_close_matches(title, symbol_map.keys(), n=1, cutoff=0.5)
    if best_match:
        return symbol_map[best_match[0]]
    return None

def get_stock_info(symbol):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}"
        }
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers, timeout=5)
        res = session.get(url, headers=headers, timeout=5)
        data = res.json()

        name = data["info"]["companyName"]
        ltp = float(data["priceInfo"]["lastPrice"])
        change = float(data["priceInfo"]["pChange"])

        arrow = "↑" if change >= 0 else "↓"
        return f"**{name}** at ₹{ltp:.2f} ({arrow} {change:+.2f}%)"
    except Exception as e:
        print(f"Error fetching stock info for {symbol}: {e}")
        return None

# Load map on module import
load_symbol_map()
