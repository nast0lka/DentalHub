from pydantic import BaseModel
from typing import Optional


class SpecializationBase(BaseModel):
    name: str
    description: str


class SpecializationCreate(SpecializationBase):
    pass


class SpecializationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class SpecializationRead(SpecializationBase):
    id: int

    class Config:
        orm_mode = True
