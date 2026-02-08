from pydantic import BaseModel

class PadreCreate(BaseModel):
    nombre: str
    telefono: str

class PadreUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
