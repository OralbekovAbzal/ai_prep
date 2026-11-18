import os
from dotenv import load_dotenv

load_dotenv()

def get_db() -> str:
    return os.getenv("DATABASE_URL")