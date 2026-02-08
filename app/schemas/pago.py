from pydantic import BaseModel

class PagoCreate(BaseModel):
    fecha_id: int
    monto: float
    estado: bool

class PagoUpdate(BaseModel):
    monto: float | None = None
    estado: bool | None = None
