from typing import List
from schemas import Job

from api import site
from tasks import load_prompt

async def execute_job_finder(task: Task) -> List[Job]:
    prompt = f"{task.prompt}. {load_prompt('job_finder')}"
    jobs = await site.ask_gemini(prompt, output_format=Job)
    for job in jobs:
        job.link = await site.ask_gemini(
            f"Give me a single string containing the official specific url for the {job.job_title} position at {job.company_name}"
        )
    return jobs