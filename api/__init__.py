import base64
import asyncio
from datetime import datetime

from db.task import Task, TaskType
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from conf import config, secrets

from sites.google import Google
from tasks.job_finder import execute_job_finder

api = FastAPI(root_path="/api")

api.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.allow_origins,
    allow_methods=config.cors.allow_methods,
    allow_headers=config.cors.allow_headers,
)

@api.post("/find-job")
async def ask_gemini(prompt: str):
    return await execute_job_finder(Task(prompt=prompt))

@api.post("/create-task")
def create_task(prompt: str, frequency: int, start_at: datetime, task_type: TaskType):
    Task.write(Task(prompt = prompt, start_at = start_at, frequency = frequency, task_type = task_type))

@api.get("/all-tasks")
def all_tasks():
    return Task.read()
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__init__:api", host="127.0.0.1", port=8000, reload=True)
