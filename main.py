from scanner import get_price
from mexc import get_futures_pairs

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 UwakiTrade AI is online!\n\n"
        "Available commands:\n"
        "/price BTC\n"
        "/pairs"
    )


# /price command
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n"
            "/price BTC\n"
            "/price ETH\n"
            "/price SOL"
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
        f"First 20 Pairs:\n\n"
        + "\n".join(futures_pairs[:20])
    )

    await update.message.reply_text(message)


def main():

    TOKEN = "8804940325:AAFfkhV9aKVAAHqajUDDopu5ihxP7PX-dJY"

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("pairs", pairs))

    print("🚀 Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()