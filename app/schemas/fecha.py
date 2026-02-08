from pydantic import BaseModel
from datetime import time

class FechaCreate(BaseModel):
    nino_id: int
    hora_entrada: time
    hora_salida: time

