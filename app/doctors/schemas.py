from fastapi import UploadFile
from fastapi.params import File, Form
from pydantic import BaseModel


class DoctorBase(BaseModel):
    name: str
    lastname: str
    experience: int
    specialization_id: int
    education: str
    photo: str
    dentistry_id: int
    

class DoctorForm(BaseModel):
    name: str
    lastname: str
    experience: int
    specialization_id: int
    education: str
    photo: UploadFile
    dentistry_id: int

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        lastname: str = Form(...),
        experience: int = Form(...),
        specialization_id: int = Form(...),
        education: str = Form(...),
        photo: UploadFile = File(...),
        dentistry_id: int = Form(...)
    ):
        return cls(
            name=name,
            lastname=lastname,
            experience=experience,
            specialization_id=specialization_id,
            education=education,
            photo=photo,
            dentistry_id=dentistry_id
        )
    

class DoctorInf(BaseModel):
    id: int
    name: str
    lastname: str
    
    class Config:
        from_orm = True