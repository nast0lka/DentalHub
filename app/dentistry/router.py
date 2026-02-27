from fastapi import APIRouter

from app.dentistry.dao import DentistryDAO
from app.dentistry.schemas import DentistryBase

router_dentistry = APIRouter(
    prefix="/dentistry",
    tags=["dentistry"],
)


@router_dentistry.get("")
async def get_dentistry() -> list[DentistryBase]:
    return await DentistryDAO.find_all()