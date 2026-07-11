from conf import app
from tasks_schema import read_tasks

@app.task
def test():
    print(read_tasks())
    