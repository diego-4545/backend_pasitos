from pydantic import BaseModel
from datetime import date, time

class AgendaCreate(BaseModel):
    padre_id: int
    fecha: date
    hora: time
    descripcion: str
