import base64
import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from conf import config, secrets

from sites.google import Google

api = FastAPI(root_path="/api")
api.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.allow_origins,
    allow_methods=config.cors.allow_methods,
    allow_headers=config.cors.allow_headers,
)

@api.post("/ask-gemini")
async def ask_gemini(prompt: str) -> str:
    site = Google()
    return await site.ask_gemini(prompt) or "No response received from Gemini."
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__init__:api", host="127.0.0.1", port=8000, reload=True)