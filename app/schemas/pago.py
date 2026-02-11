from pydantic import BaseModel

class PagoCreate(BaseModel):
    fecha_id: int
    deuda: float
    pago: float
    estado: bool

class PagoUpdate(BaseModel):
    deuda: float | None = None
    pago: float | None = None
    estado: bool | None = None
