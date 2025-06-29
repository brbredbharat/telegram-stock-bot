from telegram.ext import Updater, CommandHandler
import os

def start(update, context):
    update.message.reply_text("Hi! Welcome to the stock suggestion bot.\nUse /stockupdate to get today’s suggestion.")

def help_command(update, context):
    update.message.reply_text("Available commands:\n/start\n/help\n/stockupdate")

def stockupdate(update, context):
    update.message.reply_text("📈 Today's stock suggestion: RELIANCE\n(Sentiment: Positive)")

def main():
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        print("Error: TOKEN not set in environment variables.")
        return

    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("stockupdate", stockupdate))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
