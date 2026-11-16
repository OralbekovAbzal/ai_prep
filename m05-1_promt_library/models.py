from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Literal

class PromtIn(BaseModel):
    text: str = Field(min_length=5, max_length=2000)
    model: Literal["fast","pro"]
    tags: list

@dataclass
class PromtOut:
    id: int
    text: str
    model: str
    tags: list