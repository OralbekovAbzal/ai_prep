import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

def check_key(x_api_key: str | None = Header(default=None)):
    key = os.getenv("X_API_KEY")
    if key is None:
        raise HTTPException(500, "API key is not configured")
    if key != x_api_key:
        raise HTTPException(401)
