from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

scheduler = BackgroundScheduler()

# correct way
india_timezone = pytz.timezone('Asia/Kolkata')

scheduler.add_job(
    send_daily_stock_news, 
    CronTrigger(hour=9, minute=0, timezone=india_timezone)
)

scheduler.start()
