from pydantic import BaseModel



class SpecializationBase(BaseModel):
    name: str
    description: str

