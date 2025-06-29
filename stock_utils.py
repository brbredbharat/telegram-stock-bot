from nsetools import Nse
nse = Nse()

STOCK_SYMBOLS = {
    "reliance": "RELIANCE",
    "jio financial": "JIOFIN",
    "jio": "RELIANCE",
    "infosys": "INFY",
    "tcs": "TCS",
    "wipro": "WIPRO",
    "hdfc": "HDFCBANK",
    "icici": "ICICIBANK",
    "sbi": "SBIN",
    "axis": "AXISBANK",
    "indusind": "INDUSINDBK",
    "bajaj finance": "BAJFINANCE",
    "bajaj": "BAJFINANCE",
    "lt": "LT",
    "larsen": "LT",
    "hcl": "HCLTECH",
    "ongc": "ONGC",
    "coal": "COALINDIA",
    "maruti": "MARUTI",
    "tata motors": "TATAMOTORS",
    "tata": "TATAMOTORS",
    "asian paints": "ASIANPAINT",
    "tech mahindra": "TECHM",
    "jsw": "JSWSTEEL",
    "hindalco": "HINDALCO",
    "adani": "ADANIENT",
    "power grid": "POWERGRID",
    "ntpc": "NTPC",
    "bank of baroda": "BANKBARODA",
    "bpcl": "BPCL",
    "ioc": "IOC"
}

def guess_symbol_from_title(title):
    title = title.lower()
    for keyword in STOCK_SYMBOLS:
        if keyword in title:
            return STOCK_SYMBOLS[keyword]
    return None

def get_stock_price(symbol):
    try:
        quote = nse.get_quote(symbol.lower())
        price = quote.get('lastPrice')
        change = quote.get('pChange')
        return price, change
    except Exception as e:
        print(f"Error fetching price for {symbol}:", e)
        return None, None
