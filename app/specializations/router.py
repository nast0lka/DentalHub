from datetime import date
from fastapi import APIRouter, Depends, Request

from app.specializations.models import Specialization
from app.specializations.dao import SpecializationDAO
from app.specializations.schemas import SpecializationBase

router_specialization = APIRouter(
    prefix="/specializations",
    tags=["specializations"],
)


@router_specialization.get("")
async def get_specializations() -> list[SpecializationBase]:
    return await SpecializationDAO.find_all()