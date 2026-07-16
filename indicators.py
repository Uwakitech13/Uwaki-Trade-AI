def ema(data, period):
    multiplier = 2 / (period + 1)

    ema_value = sum(data[:period]) / period

    for price in data[period:]:
        ema_value = (price - ema_value) * multiplier + ema_value

    return ema_value


def rsi(closes, period=14):

    gains = []
    losses = []

    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]

        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))
   
      
def macd(closes):

    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)

    macd_value = ema12 - ema26

    return macd_value
