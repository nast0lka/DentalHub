from datetime import date
from fastapi import APIRouter, Depends, Request

from app.doctors.dao import DoctorDAO
from app.doctors.models import Doctor
from app.doctors.schemas import DoctorBase

router_doctor = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
)


@router_doctor.get("")
async def get_doctors(request: Request):
    return await DoctorDAO.find_all()

@router_doctor.get("/by-specialization/{specialization_id}")
async def doctors_by_specialization(specialization_id: int):
    doctors = await DoctorDAO.get_doctor_by_specialization(specialization_id)
    return [
        {
            "id": d.id,
            "name": f"{d.name} {d.lastname}"
        }
        for d in doctors
    ]

@router_doctor.get("/{doctor_id}/occupied-slots")
async def occupied_slots(doctor_id: int, date: date):
    slots = await DoctorDAO.availability_check(doctor_id)
    return [
        s["time"].strftime("%H:%M")
        for s in slots
        if s["date"] == date
    ]