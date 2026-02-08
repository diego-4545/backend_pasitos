from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import verificar_api_key
from app.models.padre import Padre
from app.schemas.padre import PadreCreate, PadreUpdate

router = APIRouter(
    prefix="/padres",
    tags=["Padres"],
    dependencies=[Depends(verificar_api_key)]
)

@router.post("/")
def crear_padre(padre: PadreCreate, db: Session = Depends(get_db)):
    nuevo = Padre(**padre.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/")
def listar_padres(db: Session = Depends(get_db)):
    return db.query(Padre).all()

@router.put("/{padre_id}")
def actualizar_padre(padre_id: int, padre: PadreUpdate, db: Session = Depends(get_db)):
    registro = db.query(Padre).filter(Padre.id == padre_id).first()
    if not registro:
        raise HTTPException(404, "Padre no encontrado")

    for k, v in padre.model_dump(exclude_unset=True).items():
        setattr(registro, k, v)

    db.commit()
    return registro

@router.delete("/{padre_id}")
def eliminar_padre(padre_id: int, db: Session = Depends(get_db)):
    registro = db.query(Padre).filter(Padre.id == padre_id).first()
    if not registro:
        raise HTTPException(404, "Padre no encontrado")

    db.delete(registro)
    db.commit()
    return {"mensaje": "Padre eliminado"}
