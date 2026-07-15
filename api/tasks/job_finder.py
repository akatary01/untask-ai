import requests
from typing import List
from schemas import Job
from db.user import User
from db.task import Task
from tasks import load_prompt

from vars import site_google

async def execute_job_finder(user_prompt: str, timeout: int = 30) -> List[Job]:
    prompt = f"{user_prompt}. {load_prompt('job_finder')}"
    jobs = await site_google.ask_gemini_json(prompt, output_format=Job, timeout=timeout)
    if jobs:
        # for job in jobs:
        #     job.link = await site_google.ask_gemini(
        #         f"Give me a single string containing the official specific url for the {job.job_title} position at {job.company_name}",
        #         timeout=timeout
        #     )
        send_email(jobs)
        return jobs
    return []

def send_email(jobs: List[Job]):
    # Define the target endpoint matching your JS URL
    url = "https://akatary.com/api/mail/contact"
    user = User.read() 

    params = {
        "name": user.name,       
        "email": user.email,  
        
        "message": f"{jobs}",       
        
        "fromEmail": "akatary23@gmail.com",
        "fromEmailConfirm": "akatary23@gmail.com",
        # Pass multiple emails as separate query parameters if needed
        "reciepientEmails": [user.email], 
        "subject": "Found Jobs"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # requests.get automatically encodes the dictionary into ?key=value& URL strings
        response = requests.get(url, params=params, headers=headers)
        
        # Print the final URL to verify the query string encoding
        print("Requested URL:", response.url)
        
        if response.status_code == 200:
            print("Success! Message sent.")
            print("Response:", response.text)
        else:
            print(f"Failed. Status code: {response.status_code}")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
