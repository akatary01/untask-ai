from conf.celery_app import app


@app.task
def test():
    print("test: its workingggg")
    

