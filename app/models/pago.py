from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    estado = Column(Integer, nullable=False)  # 0 = no pagado, 1 = pagado

    fecha_id = Column(Integer, ForeignKey("fechas.id"), nullable=False)

    fecha = relationship("Fecha")
