from sqlalchemy import Column, Integer, String
from app.database import Base

class Maestro(Base):
    __tablename__ = "maestros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
