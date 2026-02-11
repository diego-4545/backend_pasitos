from pydantic import BaseModel
from datetime import time

class FechaCreate(BaseModel):
    nino_id: int
    tiempo_estancia: int
    hora_entrada: time
    hora_salida: time

