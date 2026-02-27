from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.appointments.models import Appointment
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.dao import UserDAO


class AppointmentDAO(BaseDAO):
    model = Appointment

    @classmethod
    async def find_all_by_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(Appointment).options(
                selectinload(Appointment.doctor),
                selectinload(Appointment.service)
            ).where(Appointment.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()

    