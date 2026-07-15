import argparse
from datetime import datetime 
from db.task import Task, TaskType

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A sample CLI script")
    parser.add_argument("-p", "--prompt", type=str)
    parser.add_argument("-f", "--frequency", type=int, default=1)
    
    parser.add_argument("-n", "--name", type=str)
    parser.add_argument("-e", "--email", type=str)
    
    args = parser.parse_args()
    
    if args.name:
        User.update_name(name) # TODO: @Eemzz 
    if args.email:
        User.update_email(email) # TODO: @Eemzz, test command: python3 main.py -e atkatary@gmail.com -n "Ahmed Katary" -p "find software engineering jobs near palo alto"
        
    Task.write(Task(prompt=args.prompt, start_at=datetime.now(), frequency=args.frequency, task_type=TaskType.JOB_FINDER))