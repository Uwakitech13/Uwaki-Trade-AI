import requests

def get_price(symbol):
    symbol = symbol.upper() + "USDT"

    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if "price" not in data:
        return None

    return data["price"]