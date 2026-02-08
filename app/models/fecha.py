from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Fecha(Base):
    __tablename__ = "fechas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)

    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    tiempo_estancia = Column(Integer, nullable=False)

    nino_id = Column(Integer, ForeignKey("ninos.id"), nullable=False)

    nino = relationship("Nino")
