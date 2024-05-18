from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification as noti
import sys
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

from reminder.models import Reminder

# This is the function you want to schedule - add as many as you want and then register them in the start() function below


def send_notification_reminder():
    print("START")
    reminders = Reminder.objects.all()
    for reminder in reminders:
        now = datetime.now()
        if reminder.type == 'daily':
            now = now.strftime('%H:%M')
            time = reminder.date_time.strftime('%H:%M')
            devices = FCMDevice.objects.filter(user=reminder.user)
            if (now == time):
                devices = FCMDevice.objects.filter(user=reminder.user)
                devices.send_message(
                    message=Message(
                        notification=noti(
                            title=reminder.farm.title,
                            body=reminder.description
                        ),
                    ),
                )
                print("NOTIFICATION SENT DAILY")
        elif reminder.type == 'weekly':
            now = now.strftime('%A:%H:%M')
            time = reminder.date_time.strftime('%A:%H:%M')
            if (now == time):
                devices = FCMDevice.objects.filter(user=reminder.user)
                devices.send_message(
                    message=Message(
                        notification=noti(
                            title=reminder.farm.title,
                            body=reminder.description
                        ),
                    ),
                )
        elif reminder.type == 'monthly':
            now = now.strftime('%d:%H:%M')
            time = reminder.date_time.strftime('%d:%H:%M')
            if now == time:
                devices = FCMDevice.objects.filter(user=reminder.user)
                devices.send_message(
                    message=Message(
                        notification=noti(
                            title=reminder.farm.title,
                            body=reminder.description
                        ),
                    ),
                )
    print("END")


def start():
    scheduler = BackgroundScheduler()
    scheduler.remove_all_jobs()
    # scheduler.add_jobstore(DjangoJobStore(), "default")
    # run this job every 24 hours
    try:
        trigger = CronTrigger(
            year="*", month="*", day="*", hour="*", minute="*", second="0"
        )
        scheduler.add_job(send_notification_reminder,
                          trigger=trigger, minutes=1)
    except Exception as e:
        print(f"Failed to add job: {e}")
        raise
    scheduler.start()
    print("Scheduler started...", file=sys.stdout)
