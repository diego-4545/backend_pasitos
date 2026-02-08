from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Nino(Base):
    __tablename__ = "ninos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    padre_id = Column(Integer, ForeignKey("padres.id"), nullable=False)

    padre = relationship("Padre")
