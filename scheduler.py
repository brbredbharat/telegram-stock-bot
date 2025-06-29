from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

# Dummy version of send_daily_stock_news (replace with real logic later)
def send_daily_stock_news():
    print("Sending daily stock news...")
    # This is where you'll fetch news, analyze sentiment, and send it via Telegram.

def schedule_daily_job():
    scheduler = BackgroundScheduler()
    ist = pytz.timezone('Asia/Kolkata')
    scheduler.add_job(send_daily_stock_news, CronTrigger(hour=9, minute=0, timezone=ist))
    scheduler.start()
