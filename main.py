from telegram.ext import Updater, CommandHandler
import logging
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace this with your real logic
def start(update, context):
    update.message.reply_text("Hello! I'm your stock suggestion bot. Use /stockupdate to get today's recommendation.")

def help_command(update, context):
    update.message.reply_text("Use /stockupdate to get the stock suggestion for today.")

def stockupdate(update, context):
    update.message.reply_text("📈 Suggested stock for today: RELIANCE\nReason: Positive news sentiment and strong volume.")

def main():
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        logger.error("TOKEN environment variable not set.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("stockupdate", stockupdate))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
