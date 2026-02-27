from typing import Optional

from pydantic import BaseModel


class DentistryBase(BaseModel):
    address: str
    phone: str
    city: str


class DentistryCreate(DentistryBase):
    pass


class DentistryUpdate(BaseModel):
    address: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None


class DentistryRead(DentistryBase):
    id: int

    class Config:
        orm_mode = True
