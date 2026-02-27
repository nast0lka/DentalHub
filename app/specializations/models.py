from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    doctors = relationship("Doctor", back_populates="specialization")
    services = relationship("Service", back_populates="specialization")

    def __str__(self):
        return  f"{self.name}"