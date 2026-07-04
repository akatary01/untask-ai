from typing import List

from pydantic import BaseModel

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
