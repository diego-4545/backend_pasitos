from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)

    deuda = Column(Float, nullable=False)  
    pago = Column(Float, nullable=False)    
    estado = Column(Integer, nullable=False) 

    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)

    nino_id = Column(Integer, ForeignKey("ninos.id"), nullable=False)

    nino = relationship("Nino")