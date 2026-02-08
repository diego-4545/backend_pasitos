from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from app.database import Base

class Agenda(Base):
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    descripcion = Column(String, nullable=False)

    padre_id = Column(Integer, ForeignKey("padres.id"), nullable=False)
