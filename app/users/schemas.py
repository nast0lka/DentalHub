from fastapi.params import Form
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class UserBase(BaseModel):
    name: str
    lastname: str
    age: date
    email: EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        lastname: str = Form(...),
        age: date = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...)
    ):
        return cls(
            name=name,
            lastname=lastname,
            age=age,
            email=email,
            password=password
        )




class SUserAuth(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        password: str = Form(...)
    ):
        return cls(
            email=email,
            password=password
        )

    class Config:
        orm_mode = True
