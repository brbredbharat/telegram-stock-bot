import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /stock to get today's stock tip.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start – Welcome\n/help – Command list\n/stock – Daily stock tip")

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Today's stock tip: *HDFC Bank* – Strong Buy", parse_mode="Markdown")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("stock", stock))

print("🤖 Bot is running...")
app.run_polling()
