import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Read your bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /stock to get today's stock tip.")

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 Available commands:\n/start\n/help\n/stock")

# Command: /stock
async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Today's stock tip: *HDFC Bank* – Strong Buy", parse_mode="Markdown")

# Main function
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stock", stock))

    print("🤖 Bot is running...")
    app.run_polling()
