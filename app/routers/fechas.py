from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import verificar_api_key
from app.models.fecha import Fecha
from app.schemas.fecha import FechaCreate

router = APIRouter(
    prefix="/fechas",
    tags=["Fechas"],
    dependencies=[Depends(verificar_api_key)]
)

@router.post("/")
def crear_fecha(fecha: FechaCreate, db: Session = Depends(get_db)):
    nueva = Fecha(**fecha.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/")
def listar_fechas(db: Session = Depends(get_db)):
    return db.query(Fecha).all()
