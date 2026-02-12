from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.orm import relationship


from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    age = Column(Date, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    is_admin = Column(Boolean, default=False)

    appointments = relationship("Appointment", back_populates="user")

    def __str__(self):
        return  f"{self.name} {self.lastname}"