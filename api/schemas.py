from pydantic import BaseModel
from typing import List, Optional

## conf ##
class Cors(BaseModel):
    allow_origins: List[str]
    allow_methods: List[str]
    allow_headers: List[str]

class Config(BaseModel):
    cors: Cors

class Secrets(BaseModel):
    google_api_key: str
    browser_use_api_key: str

## tasks ## 
class Job(BaseModel):
    company_name: str
    job_title: str
    
    salary_range: str
    description: str
    work_arrangement: str
    min_requirements: str
    job_location: str
    
    link: Optional[str]