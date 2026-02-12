from datetime import datetime
from app.appointments.models import Appointment
from app.dao.base import BaseDAO
from app.doctors.models import Doctor
from app.database import async_session_maker
from sqlalchemy import and_, func, insert, or_, select

class DoctorDAO(BaseDAO):
    model = Doctor

    @classmethod
    async def availability_check(cls, doctor_id: int):
        now = datetime.now()
        async with async_session_maker() as session:
            occupied_slots = (
                    select(Appointment.date, Appointment.time)
                    .where(
                        Appointment.doctor_id == doctor_id,
                        Appointment.date >= now.date()
                    ))

            result = await session.execute(occupied_slots)
            slots = result.all()

            return [
                {
                    "date": slot.date,
                    "time": slot.time
                }
                for slot in slots
            ]
        
    @classmethod
    async def get_doctor_by_specialization(cls, specialization_id: int):
        async with async_session_maker() as session:
            query = select(Doctor).where(Doctor.specialization_id == specialization_id)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def doctor_add(cls, doctor_data: dict) -> Doctor:
        doctor = cls.model(**doctor_data)
        async with async_session_maker() as session:
            session.add(doctor)
            await session.commit()
            await session.refresh(doctor)
            return doctor