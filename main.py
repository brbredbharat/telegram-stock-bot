from telegram.ext import Updater, CommandHandler
from news_fetcher import get_top_3_stocks
from scheduler import schedule_daily_job
import os

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Welcome! Use /getstocks to fetch today's stock suggestions.")

def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="/start\n/help\n/getstocks")

def getstocks(update, context):
    message = get_top_3_stocks()
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="Markdown")

def main():
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        print("Error: TOKEN not set in environment variables.")
        return

    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("getstocks", getstocks))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    schedule_daily_job()
    main()
