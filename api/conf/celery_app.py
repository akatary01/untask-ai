from celery import Celery
import os
from celery.schedules import crontab
from datetime import timedelta

app = Celery(
    'conf',  # application name
    broker = 'redis://localhost:6379/0',
    backend = 'redis://localhost:6379/0',
    include=['tasks']  # Auto-discover tasks from these modules
)


app.conf.beat_schedule = {
    # Run every 1s
    'test': {
        'task': 'tasks.test',
        'schedule': timedelta(seconds=1),  # Every 1 second
    }
}   