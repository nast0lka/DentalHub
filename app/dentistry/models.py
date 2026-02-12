from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Dentistry(Base):
    __tablename__ = "dentistry"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    city = Column(String, nullable=False)
    
    doctors = relationship("Doctor", back_populates="dentistry")

    def __str__(self):
        return  f"{self.address}"
