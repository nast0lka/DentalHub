from fastapi.params import Form
from pydantic import BaseModel
from datetime import date, time
from typing import Optional


from pydantic import BaseModel
from fastapi import Form
from datetime import datetime, date, time

class AppointmentBase(BaseModel):
    date: date
    time: time
    doctor_id: int
    service_id: int

    @classmethod
    def as_form(
        cls,
        date: str = Form(...),
        time: str = Form(...),
        doctor_id: int = Form(...),
        service_id: int = Form(...),
    ):
        return cls(
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            time=datetime.strptime(time, "%H:%M").time(),
            doctor_id=doctor_id,
            service_id=service_id
        )


