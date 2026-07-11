from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from scanner import get_price

TOKEN = "8804940325:AAFfkhV9aKVAAHqajUDDopu5ihxP7PX-dJY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is online!")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Usage:\n/price BTC\n/price ETH\n/price SOL"
        )
        return

    coin = context.args[0].upper()

    current_price = get_price(coin)

    if current_price is None:
        await update.message.reply_text("❌ Coin not found.")
        return

    await update.message.reply_text(
        f"📊 {coin}USDT\n\n"
        f"💰 Current Price: ${current_price}"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    print("🚀 Bot is running...")

    app.run_polling()

if __name__ == "__main__":
    main()