from pydantic import BaseModel

class NinoCreate(BaseModel):
    nombre: str
    edad: int
    padre_id: int

class NinoUpdate(BaseModel):
    nombre: str | None = None
    edad: int | None = None
    padre_id: int | None = None
