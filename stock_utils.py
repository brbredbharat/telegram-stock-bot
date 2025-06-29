import requests
import re

# Minimal symbol map (you can expand or load from NSE file)
SYMBOL_MAP = {
    "reliance": "RELIANCE",
    "tcs": "TCS",
    "infosys": "INFY",
    "hdfc bank": "HDFCBANK",
    "larsen": "LT",
    "indusind": "INDUSINDBK",
    "torrent": "TORNTPHARM",
    "dixon": "DIXON",
    "akzo": "AKZOINDIA",
    "nykaa": "FSN",
    "indigo": "INDIGO",
    "varun beverages": "VBL",
}

def guess_symbol_from_title(title):
    title = title.lower()
    for name, symbol in SYMBOL_MAP.items():
        if name in title:
            return symbol
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

        return {
            "name": name,
            "ltp": ltp,
            "changePercent": change
        }
    except Exception as e:
        print(f"Stock info error for {symbol}: {e}")
        return None
