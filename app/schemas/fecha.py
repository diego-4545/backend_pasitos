from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class FechaCreate(BaseModel):
    fecha: date
    nino_id: int
    hora_inicio: time
    hora_fin: Optional[time] = None
    tiempo_estancia: Optional[int] = None

class FechaUpdate(BaseModel):
    fecha: Optional[date] = None
    nino_id: Optional[int] = None
    tiempo_estancia: Optional[int] = None        
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None