from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import verificar_api_key
from app.models.agenda import Agenda
from app.schemas.agenda import AgendaCreate

router = APIRouter(
    prefix="/agenda",
    tags=["Agenda"],
    dependencies=[Depends(verificar_api_key)]
)

@router.post("/")
def crear_cita(cita: AgendaCreate, db: Session = Depends(get_db)):
    nueva = Agenda(**cita.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/")
def listar_citas(db: Session = Depends(get_db)):
    return db.query(Agenda).all()

@router.delete("/{cita_id}")
def eliminar_cita(cita_id: int, db: Session = Depends(get_db)):
    registro = db.query(Agenda).filter(Agenda.id == cita_id).first()
    if not registro:
        raise HTTPException(404, "Cita no encontrada")

    db.delete(registro)
    db.commit()
    return {"mensaje": "Cita eliminada"}
