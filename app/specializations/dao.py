from app.dao.base import BaseDAO
from app.specializations.models import Specialization

class SpecializationDAO(BaseDAO):
    model = Specialization