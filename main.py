import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    data = {"contents": [{"parts": [{"text": text}]}]}
    try:
        r = requests.post(url, json=data, timeout=30)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Gemini Error:", e)
        return "AI ektu busy, ektu pore abar try koro."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalamu Alaikum Shaon! Ami tomar bot. Ami ekhon live achi ✅\n\nAmake kichu likho, ami reply dibo.")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    ans = ask_gemini(text)
    await update.message.reply_text(ans)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

flask_app = Flask(__name__)
@flask_app.route("/")
def home():
    return "Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app.run_polling(stop_signals=None)
