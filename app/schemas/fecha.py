from pydantic import BaseModel
from datetime import time
from typing import Optional

class FechaCreate(BaseModel):
    nino_id: int
    tiempo_estancia: int
    hora_entrada: time
    hora_salida: time


class FechaUpdate(BaseModel):
    nino_id: Optional[int] = None
    tiempo_estancia: Optional[int] = None        
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None