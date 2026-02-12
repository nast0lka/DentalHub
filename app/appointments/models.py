from sqlalchemy import Column, Date, Integer, String, ForeignKey, Time
from app.database import Base
from sqlalchemy.orm import relationship


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    doctor = relationship("Doctor", back_populates="appointments")
    user = relationship("User", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")

    def __str__(self):
        return  f"Запись №{self.id} на {self.date} {self.time}"

