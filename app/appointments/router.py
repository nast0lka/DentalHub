from datetime import date, datetime
from time import time
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.users.auth import get_current_user
from app.appointments.schemas import AppointmentBase
from app.appointments.dao import AppointmentDAO
from app.appointments.models import Appointment

from starlette.status import HTTP_303_SEE_OTHER

router_appointment = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
)

@router_appointment.post("/create")
async def create_appointment(
    request: Request,
    appointment_data: AppointmentBase = Depends(AppointmentBase.as_form)
):
    user = await get_current_user(request)
    if not user:
        raise Exception("Authentication required")

    await AppointmentDAO.add(
        user_id=user.id,
        date=appointment_data.date,
        time=appointment_data.time,
        doctor_id=appointment_data.doctor_id,
        service_id=appointment_data.service_id,
    )

    return RedirectResponse("/", status_code=303)

@router_appointment.get("/my-appointments")
async def get_user_appointments(user=Depends(get_current_user)):
    appointments = await AppointmentDAO.find_all_by_user(user.id)
    return appointments

@router_appointment.get("/{appointment_id}/cancel")
async def cancel_appointment(appointment_id: int, user=Depends(get_current_user)):
    appointment = await AppointmentDAO.find_one_or_none(id=appointment_id)
    if appointment and appointment.user_id == user.id:
        await AppointmentDAO.delete(id=appointment_id)
    return RedirectResponse("/profile", status_code=HTTP_303_SEE_OTHER)