import os
from dotenv import load_dotenv

from scanner import get_price
from mexc import get_futures_pairs
from strategy import scan_market

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

# Get Telegram Bot Token from .env
TOKEN = os.getenv("BOT_TOKEN")


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 UwakiTrade AI Online\n\n"
        "Available Commands:\n"
        "/price BTC\n"
        "/pairs\n"
        "/scan"
    )


# /price command
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n"
            "/price BTC"
        )
        return

    coin = context.args[0].upper()

    result = get_price(coin)

    if result is None:
        await update.message.reply_text("❌ Coin not found.")
        return

    await update.message.reply_text(
        f"📊 {coin}USDT\n\n"
        f"💰 Price: ${result}"
    )


# /pairs command
async def pairs(update: Update, context: ContextTypes.DEFAULT_TYPE):

    futures_pairs = get_futures_pairs()

    message = (
        f"📈 MEXC Futures\n\n"
        f"Total Futures Pairs: {len(futures_pairs)}\n\n"
        + "\n".join(futures_pairs[:20])
    )

    await update.message.reply_text(message)


# /scan command
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔍 Scanning MEXC Futures...\nPlease wait..."
    )

    signals = scan_market()

    if len(signals) == 0:
        await update.message.reply_text("❌ No Strong Buy signals found.")
        return

    message = "🔥 UwakiTrade AI Signals 🔥\n\n"

    for signal in signals[:10]:

        message += (
            f"📈 {signal['symbol']}\n"
            f"💰 Price: {signal['price']}\n"
            f"📊 EMA20: {signal['ema20']}\n"
            f"📊 EMA50: {signal['ema50']}\n"
            f"📈 RSI: {signal['rsi']}\n"
            f"📉 MACD: {signal['macd']}\n"
            f"🚦 Trend: {signal['trend']}\n\n"
        )

    message += f"✅ Total Strong Buy Signals: {len(signals)}"

    await update.message.reply_text(message)


def main():

    if not TOKEN:
        print("❌ BOT_TOKEN not found in .env file")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("pairs", pairs))
    app.add_handler(CommandHandler("scan", scan))

    print("🚀 UwakiTrade AI Running...")

    app.run_polling()


if __name__ == "__main__":
    main()