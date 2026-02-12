from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)
    specialization_id = Column(Integer, ForeignKey("specializations.id"), nullable=False)
    education = Column(String, nullable=False)
    photo = Column(String, nullable=False)

    dentistry_id = Column(Integer, ForeignKey("dentistry.id"), nullable=False)

    dentistry = relationship("Dentistry", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor")
    specialization = relationship("Specialization", back_populates="doctors")

    def __str__(self):
        return  f"{self.name} {self.lastname}"
    