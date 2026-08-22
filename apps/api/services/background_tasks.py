from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apps.api.source.configuration import Settings
from apps.api.services.mail_service import send_email
from datetime import datetime
from zoneinfo import ZoneInfo

jobstore = SQLAlchemyJobStore(url=Settings.DATABASE_URL)
scheduler = BackgroundScheduler(jobstores={'default': jobstore}, timezone=ZoneInfo("Asia/Kolkata"))

scheduler.start()

def add_background_mail(to_email: str, subject: str, description: str, send_time: datetime, id: int ):
    print(send_time)
    print(send_time.tzinfo)
    scheduler.add_job(send_email, 'date', run_date=send_time,id=str(id), kwargs={'to_email': to_email, 'subject': subject, 'description': description})


def add_daily_background_mail(to_email: str, subject: str, description: str, send_time: datetime, id: int ):
    scheduler.add_job(send_email, 'interval', days=1, start_date=send_time, id=str(id), kwargs={'to_email': to_email, 'subject': subject, 'description': description})


def add_weekly_background_mail(to_email: str, subject: str, description: str, send_time: datetime, id: int ):
    scheduler.add_job(send_email, 'interval', weeks=1, start_date=send_time, id=str(id), kwargs={'to_email': to_email, 'subject': subject, 'description': description})


def add_monthly_background_mail(to_email: str, subject: str, description: str, send_time: datetime, id: int ):
    day = send_time.day
    hour = send_time.hour
    minute = send_time.minute
    scheduler.add_job(send_email, 'cron', day=day, hour=hour, minute=minute, start_date=send_time, id=str(id), kwargs={'to_email': to_email, 'subject': subject, 'description': description})


def remove_background_mail(id: int):
    try:
        scheduler.remove_job(str(id))
    except Exception as e:
        print(f"Error removing job: {e}")  
