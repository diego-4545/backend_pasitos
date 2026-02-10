from pydantic import BaseModel

class MaestroCreate(BaseModel):
    nombre: str
    telefono: str
    username: str
    password: str
    sucursal: int

class MaestroUpdate(BaseModel):
    nombre: str | None = None
    telefono: str | None = None
    username: str | None = None
    password: str | None = None
    sucursal: int | None = None
