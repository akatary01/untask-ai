from conf import app
from db.task import Task

@app.task
def test():
    print(Task.read())
    