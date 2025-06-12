# bot/telegram_bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from search import search_books

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 ¡Hola! Enviame el título de un libro y te diré si lo encuentro.")

# Manejo de mensajes comunes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    resultado = search_books(texto)
    await update.message.reply_text(resultado)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
