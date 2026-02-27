from app.dao.base import BaseDAO
from app.services.models import Service


class ServicesDAO(BaseDAO):
    model = Service
