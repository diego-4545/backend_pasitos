from pydantic import BaseModel

class MaestroCreate(BaseModel):
    nombre: str
    telefono: str
    password: str

class MaestroUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    password: str | None = None
