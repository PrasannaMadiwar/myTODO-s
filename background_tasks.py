from apscheduler.schedulers.background import BackgroundScheduler
from mail_service import send_email
from datetime import datetime
from zoneinfo import ZoneInfo


scheduler = BackgroundScheduler(
    timezone=ZoneInfo("Asia/Kolkata")
)

scheduler.start()

def add_background_mail(to_email: str, subject: str, description: str, send_time: datetime):
    print(send_time)
    print(send_time.tzinfo)
    scheduler.add_job(send_email, 'date', run_date=send_time, kwargs={'to_email': to_email, 'subject': subject, 'description': description})