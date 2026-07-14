import ccxt

exchange = ccxt.mexc({
    "options": {
        "defaultType": "swap"   # Use Futures market
    }
})

def get_futures_pairs():
    markets = exchange.load_markets()

    pairs = []

    for symbol, market in markets.items():
        if market.get("swap") and market.get("quote") == "USDT":
            pairs.append(symbol)

    return sorted(pairs)
