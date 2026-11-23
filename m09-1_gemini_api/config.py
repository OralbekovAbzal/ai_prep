import os
from dotenv import load_dotenv

load_dotenv()

def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY")

def get_db_url() -> str:
    return os.getenv("DATABASE_URL")