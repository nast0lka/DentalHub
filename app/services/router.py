from fastapi import APIRouter

from app.services.dao import ServicesDAO
from app.services.models import Service
from app.services.schemas import ServiceBase

router_service = APIRouter(
    prefix="/services",
    tags=["services"],
)


@router_service.get("")
async def get_services() -> list[ServiceBase]:
    return await ServicesDAO.find_all()