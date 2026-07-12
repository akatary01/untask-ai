from conf import app
from db.task import Task

@app.task
def test():
    all_tasks = Task.read()
    return 

