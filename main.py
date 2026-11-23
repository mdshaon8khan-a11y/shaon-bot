import os, requests, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalamu Alaikum Shaon! Ami tomar bot. Ami ekhon live achi ✅\n\nAmake kichu likhe pathao, ami reply dibo.")

def ask_gemini(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    data = {"contents": [{"parts": [{"text": question}]}]}
    try:
        r = requests.post(url, json=data, timeout=20)
        j = r.json()
        if "candidates" not in j:
            print("GEMINI ERROR:", j)
            return "AI ektu busy, 1 min por abar likho Shaon!"
        return j["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Ektu somossa hoiche Shaon, abar chesta koro! ({e})"

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = ask_gemini(update.message.text)
    await update.message.reply_text(ans)

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"Bot is Live!")
    def log_message(self, *a): pass

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), H).serve_forever()
