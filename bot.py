import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TG_TOKEN = os.getenv("TG_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши, какой фильм ты ищешь — я подберу тебе топ.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url).json()

    if response.get("results"):
        top = response["results"][:3]
        msg = "\n\n".join([f"{m['title']} ({m.get('release_date', '----')[:4]})\n{m.get('overview', 'Описание недоступно')[:200]}..." for m in top])
    else:
        msg = "Не нашёл ничего. Попробуй переформулировать запрос."

    await update.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token(TG_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
