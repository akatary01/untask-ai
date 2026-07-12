from conf import app
from db.task import Task
from __init__ import site



@app.task
def test():
    return 


async def job_finder_prompt(task: Task):
    prompt = task.prompt + """.  Create a json file containing 
    only listings actively accepting applicants. Format it to include the following: 
    company name, 
    job title, 
    link to job description, pulled directly from official company applicant tracking pipelines, ensuring no third-party job aggregators are included (if cannot be found exclude job), 
    job location, 
    work arrangement (remote, hybrid, onsite), 
    salary range, 
    brief description of job, 
    list of minimum requirements for job."""
    return await site.ask_gemini(prompt)

async def find_job_link(company_name: str, job_title: str):
    prompt =  "Give me a single string containing the official specific url for the " + job_title + " position at " + company_name 
    return await site.ask_gemini(prompt)
    