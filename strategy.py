import ccxt
from indicators import ema, rsi, macd
from mexc import get_futures_pairs

# Connect to MEXC Futures
exchange = ccxt.mexc({
    "options": {
        "defaultType": "swap"
    },
    "enableRateLimit": True
})


def scan_symbol(symbol):
    try:
        # Get last 100 candles
        candles = exchange.fetch_ohlcv(
            symbol,
            timeframe="15m",
            limit=100
        )

        closes = [candle[4] for candle in candles]

        # Indicators
        ema20 = ema(closes, 20)
        ema50 = ema(closes, 50)
        rsi_value = rsi(closes)
        macd_value = macd(closes)

        # Trend
        if ema20 > ema50 and rsi_value > 50 and macd_value > 0:
            trend = "🟢 Strong Buy"
        elif ema20 < ema50 and rsi_value < 50 and macd_value < 0:
            trend = "🔴 Strong Sell"
        else:
            trend = "🟡 Neutral"

        return {
            "symbol": symbol,
            "price": round(closes[-1], 2),
            "ema20": round(ema20, 2),
            "ema50": round(ema50, 2),
            "rsi": round(rsi_value, 2),
            "macd": round(macd_value, 2),
            "trend": trend
        }

    except Exception as e:
        print(f"Error scanning {symbol}: {e}")
        return None


def scan_market():
    # Scan only the first 20 pairs for testing
    pairs = get_futures_pairs()[:20]

    signals = []

    for pair in pairs:
        print(f"Scanning {pair}...")

        result = scan_symbol(pair)

        if result is None:
            continue

        # Keep only Strong Buy signals
        if result["trend"] == "🟢 Strong Buy":
            signals.append(result)

    print("Finished scanning!")

    return signals