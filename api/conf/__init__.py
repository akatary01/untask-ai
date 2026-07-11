import yaml
from celery import Celery
from datetime import timedelta
from schemas import Secrets, Config 

with open("conf/secrets.yaml") as f:
    secrets = Secrets(**yaml.safe_load(f))

with open("conf/base.yaml") as f:
    config = Config(**yaml.safe_load(f))

## celery config ##
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