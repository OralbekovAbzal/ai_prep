from pydantic import BaseModel, Field
from typing import Literal
from fastapi import HTTPException

class UserNotFound(HTTPException):
    pass

class NotEnoughCredits(HTTPException):
    pass

class Job(BaseModel):
    user_id: int = Field(gt=0)
    prompt: str = Field(min_length=5, max_length=2000)
    model: Literal["fast", "pro"]
    cost: int = Field(gt=0)