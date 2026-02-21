from pydantic import BaseModel
from typing import Optional


class SpecializationBase(BaseModel):
    name: str
    description: str

