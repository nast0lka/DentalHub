import hashlib
from datetime import date
from typing import Any, Callable, Dict, Optional, Tuple

from fastapi import APIRouter, Request, Response
from fastapi_cache.decorator import cache

from app.doctors.dao import DoctorDAO
from app.doctors.schemas import DoctorInf


def custom_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    cache_key = hashlib.md5(f"{func.__name__}:{args}:{kwargs}".encode()).hexdigest()
    return f"{namespace}:{cache_key}"

router_doctor = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
)


@router_doctor.get("")
async def get_doctors(request: Request):
    return await DoctorDAO.find_all()

@router_doctor.get("/by-specialization/{specialization_id}", response_model=list[DoctorInf])
@cache(expire=100, key_builder=custom_key_builder)
async def doctors_by_specialization(specialization_id: int, request: Request):
    return await DoctorDAO.get_doctor_by_specialization(specialization_id)

@router_doctor.get("/{doctor_id}/occupied-slots")
async def occupied_slots(doctor_id: int, date: date):
    slots = await DoctorDAO.availability_check(doctor_id)
    return [
        s["time"].strftime("%H:%M")
        for s in slots
        if s["date"] == date
    ]