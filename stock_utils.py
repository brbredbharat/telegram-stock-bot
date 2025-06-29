import yfinance as yf

def guess_symbol_from_title(title):
    # A simple matching based on common stock tickers; you can expand this
    known_stocks = {
        "Reliance": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "Infosys": "INFY.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI": "ICICIBANK.NS",
        "Larsen": "LT.NS",
        "HUL": "HINDUNILVR.NS",
        "SBI": "SBIN.NS",
        "Kotak": "KOTAKBANK.NS",
        "Bharti": "BHARTIARTL.NS",
        "Adani": "ADANIENT.NS",
        "Wipro": "WIPRO.NS",
        "Tata Steel": "TATASTEEL.NS",
        "Tata Motors": "TATAMOTORS.NS"
    }

    for key, symbol in known_stocks.items():
        if key.lower() in title.lower():
            return symbol
    return None

def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        latest = data.iloc[-1]
        previous = data.iloc[-2]
        ltp = latest["Close"]
        prev = previous["Close"]
        change_percent = ((ltp - prev) / prev) * 100
        return {
            "name": symbol,
            "ltp": ltp,
            "changePercent": change_percent
        }
    except Exception as e:
        print(f"Error fetching stock info for {symbol}: {e}")
        return None
