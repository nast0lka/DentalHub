from app.dao.base import BaseDAO
from app.dentistry.models import Dentistry


class DentistryDAO(BaseDAO):
    model = Dentistry
