from typing import Optional

from pydantic import BaseModel


class ServiceBase(BaseModel):
    name: str
    description: str
    price: int
    requires_consultation: bool
    specialization_id: int


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    price: Optional[int] = None
    requires_consultation: Optional[bool] = None
    specialization_id: Optional[int] = None


class ServiceRead(ServiceBase):
    id: int

    class Config:
        orm_mode = True
