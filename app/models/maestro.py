from sqlalchemy import Column, Integer, String
from app.database import Base

class Maestro(Base):
    __tablename__ = "maestros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    sucursal = Column(Integer, nullable=False)

