from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from news_fetcher import get_top_3_stocks
import os

def send_daily_stock_news():
    TOKEN = os.environ.get("TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")
    if not TOKEN or not CHAT_ID:
        print("TOKEN or CHAT_ID not set")
        return

    bot = Bot(token=TOKEN)
    message = get_top_3_stocks()
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def schedule_daily_job():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_stock_news, trigger='cron', hour=9, minute=0)
    scheduler.start()
