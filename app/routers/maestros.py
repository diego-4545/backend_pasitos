from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import verificar_api_key
from app.models.maestro import Maestro
from app.schemas.maestro import MaestroCreate, MaestroUpdate

router = APIRouter(
    prefix="/maestros",
    tags=["Maestros"],
    dependencies=[Depends(verificar_api_key)]
)

@router.post("/")
def crear_maestro(maestro: MaestroCreate, db: Session = Depends(get_db)):
    nuevo = Maestro(**maestro.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/")
def listar_maestros(db: Session = Depends(get_db)):
    return db.query(Maestro).all()

@router.put("/{maestro_id}")
def actualizar_maestro(maestro_id: int, maestro: MaestroUpdate, db: Session = Depends(get_db)):
    registro = db.query(Maestro).filter(Maestro.id == maestro_id).first()
    if not registro:
        raise HTTPException(404, "Maestro no encontrado")

    for k, v in maestro.model_dump(exclude_unset=True).items():
        setattr(registro, k, v)

    db.commit()
    return registro

@router.delete("/{maestro_id}")
def eliminar_maestro(maestro_id: int, db: Session = Depends(get_db)):
    registro = db.query(Maestro).filter(Maestro.id == maestro_id).first()
    if not registro:
        raise HTTPException(404, "Maestro no encontrado")

    db.delete(registro)
    db.commit()
    return {"mensaje": "Maestro eliminado"}
