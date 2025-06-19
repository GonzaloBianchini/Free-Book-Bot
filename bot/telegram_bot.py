# bot/telegram_bot.py


from dotenv import load_dotenv
import json
import os

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes,CallbackQueryHandler
from telegram import Update
from handlers import handle_message,manejar_callback


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 ¡Hola! Enviame el título de un libro y te diré si lo encuentro.")



def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(manejar_callback))

    print("🤖 Bot iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()
