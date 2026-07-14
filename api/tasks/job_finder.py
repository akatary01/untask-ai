from typing import List
from schemas import Job

from db.task import Task
from tasks import load_prompt

from vars import site_google

async def execute_job_finder(task: Task, timeout: int = 30) -> List[Job]:
    prompt = f"{task.prompt}. {load_prompt('job_finder')}"
    jobs = await site_google.ask_gemini_json(prompt, output_format=Job, timeout=timeout)
    if jobs:
        for job in jobs:
            job.link = await site_google.ask_gemini(
                f"Give me a single string containing the official specific url for the {job.job_title} position at {job.company_name}",
                timeout=timeout
            )
        return jobs
    return []