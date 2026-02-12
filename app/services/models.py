from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    specialization_id = Column(Integer, ForeignKey("specializations.id"), nullable=False)

    specialization = relationship("Specialization", back_populates="services")
    appointments = relationship("Appointment", back_populates="service", cascade="all, delete-orphan")

    def __str__(self):
        return  f"{self.name}"