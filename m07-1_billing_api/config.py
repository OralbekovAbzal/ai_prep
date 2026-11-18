import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

def get_db() -> str:
    return os.getenv("DATABASE_URL")

def check_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != os.getenv("KEY"):
        raise HTTPException(401)