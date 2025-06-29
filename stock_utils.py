from nsetools import Nse
nse = Nse()

def get_stock_price(symbol):
    try:
        q = nse.get_quote(symbol.lower())
        price = q['lastPrice']
        change = q['pChange']
        return price, change
    except Exception as e:
        return None, None

# Simplified mapping of common company names to NSE symbols
STOCK_SYMBOLS = {
    "reliance": "RELIANCE",
    "tcs": "TCS",
    "infosys": "INFY",
    "wipro": "WIPRO",
    "hdfc": "HDFCBANK",
    "icici": "ICICIBANK",
    "lt": "LT",
    "larsen": "LT",
    "tata": "TATAMOTORS",
    "jio": "RELIANCE",
    "hcl": "HCLTECH",
    "ongc": "ONGC",
    "maruti": "MARUTI",
    "coal": "COALINDIA",
    "tech mahindra": "TECHM",
    "sbi": "SBIN"
}

def guess_symbol_from_title(title):
    title = title.lower()
    for key in STOCK_SYMBOLS:
        if key in title:
            return STOCK_SYMBOLS[key]
    return None
