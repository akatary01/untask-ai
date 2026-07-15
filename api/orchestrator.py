import asyncio
from datetime import datetime, timedelta

from conf import app
from db.task import Task, TaskType
from tasks.job_finder import execute_job_finder

@app.task
def orchestrator():
    now = datetime.now()
    for task in Task.read():
        if task.start_at + timedelta(hours=task.frequency) >= now:
            if task.type == TaskType.JOB_FINDER:
                asyncio.run(execute_job_finder(task))

