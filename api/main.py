import asyncio
import argparse
from datetime import datetime 
from db.task import Task, TaskType
from db.user import User
from tasks.job_finder import send_email, execute_job_finder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample CLI script")
    parser.add_argument("-p", "--prompt", type=str)
    parser.add_argument("-f", "--frequency", type=int, default=1)
    
    parser.add_argument("-n", "--name", type=str)
    parser.add_argument("-e", "--email", type=str)
    
    args = parser.parse_args()

    User.write(User(email=args.email, name=args.name))
    
    task = Task(prompt=args.prompt, start_at=datetime.now(), frequency=args.frequency, task_type=TaskType.JOB_FINDER)  
    task_prompt = task.prompt  # Touching the attribute forces SQLAlchemy to load it  
    Task.write(task=task)
    jobs = asyncio.run(execute_job_finder(user_prompt=task_prompt))
    # send_email(jobs=jobs) # type: ignore
    