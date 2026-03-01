from pydantic import BaseModel

class NinoCreate(BaseModel):
    nombre: str
    sucursal: int
    paquete: int  
    padre_id: int

class NinoUpdate(BaseModel):
    nombre: str | None = None
    sucursal: int | None = None
    paquete: int | None = None  
    padre_id: int | None = None