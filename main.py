import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalamu Alaikum Shaon! Ami tomar bot. Ami ekhon live achi ✅\n\nAmake kichu likhe pathao, ami reply dibo.")

async def reply_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Tumi bolso: {text}\n\nAmi tomar bot, ami shunsechi ❤️")

def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_all))
    print("Bot cholche...")
    app.run_polling()

if __name__ == "__main__":
    main()
