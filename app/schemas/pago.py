from pydantic import BaseModel
from typing import Optional


class PagoBase(BaseModel):
    nino_id: int
    mes: int
    anio: int
    deuda: float
    pago: float = 0
    estado: int = 0  


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    deuda: Optional[float] = None
    pago: Optional[float] = None
    estado: Optional[int] = None


class PagoResponse(PagoBase):
    id: int

    class Config:
        from_attributes = True