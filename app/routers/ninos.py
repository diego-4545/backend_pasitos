from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import verificar_api_key
from app.models.nino import Nino
from app.schemas.nino import NinoCreate, NinoUpdate

router = APIRouter(
    prefix="/ninos",
    tags=["Niños"],
    dependencies=[Depends(verificar_api_key)]
)

@router.post("/")
def crear_nino(nino: NinoCreate, db: Session = Depends(get_db)):
    nuevo = Nino(**nino.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/")
def listar_ninos(db: Session = Depends(get_db)):
    return db.query(Nino).all()

@router.get("/{nino_id}")
def obtener_nino(nino_id: int, db: Session = Depends(get_db)):
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise HTTPException(404, "Niño no encontrado")
    return nino

@router.put("/{nino_id}")
def actualizar_nino(nino_id: int, nino: NinoUpdate, db: Session = Depends(get_db)):
    registro = db.query(Nino).filter(Nino.id == nino_id).first()
    if not registro:
        raise HTTPException(404, "Niño no encontrado")

    for k, v in nino.model_dump(exclude_unset=True).items():
        setattr(registro, k, v)

    db.commit()
    return registro

@router.delete("/{nino_id}")
def eliminar_nino(nino_id: int, db: Session = Depends(get_db)):
    registro = db.query(Nino).filter(Nino.id == nino_id).first()
    if not registro:
        raise HTTPException(404, "Niño no encontrado")

    db.delete(registro)
    db.commit()
    return {"mensaje": "Niño eliminado"}
