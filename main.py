import os, requests, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম শাওন! আমি এখন বুদ্ধিমান 😎 যা খুশি জিজ্ঞেস করো।")

def ask_gemini(question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    data = {"contents": [{"parts": [{"text": f"তুমি শাওনের বন্ধু, বাংলায় মজা করে ছোট করে উত্তর দাও। প্রশ্ন: {question}"}]}]}
    try:
        r = requests.post(url, json=data, timeout=30)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"একটু সমস্যা হইছে শাওন, আবার চেষ্টা করো। ({e})"

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.chat.send_action("typing")
    reply = ask_gemini(text)
    await update.message.reply_text(reply[:4000])

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is live!")
        def log_message(self, *a):
            pass
    HTTPServer(("0.0.0.0", port), H).serve_forever()

if __name__ == "__main__":
    threading.Thread(target=keep_alive, daemon=True).start()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot is running...")
    app.run_polling()
