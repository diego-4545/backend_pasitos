from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import verificar_api_key
from app.models.maestro import Maestro
from app.schemas.maestro import MaestroCreate, MaestroUpdate, MaestroOut

router = APIRouter(
    prefix="/maestros",
    tags=["Maestros"],
    dependencies=[Depends(verificar_api_key)]
)

# Crear maestro
@router.post("/")
def crear_maestro(maestro: MaestroCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    usuario_existente = db.query(Maestro).filter(Maestro.username == maestro.username).first()
    if usuario_existente:
        return JSONResponse(
            status_code=200,
            content={"status": "error", "mensaje": "Usuario ya existe"}
        )

    # Crear nuevo maestro
    nuevo = Maestro(**maestro.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return JSONResponse(
        status_code=200,
        content={"status": "ok", "mensaje": "Maestro creado"}
    )

# Listar maestros
@router.get("/", response_model=list[MaestroOut])
def listar_maestros(db: Session = Depends(get_db)):
    return db.query(Maestro).all()

# Actualizar maestro
@router.put("/{maestro_id}")
def actualizar_maestro(maestro_id: int, maestro: MaestroUpdate, db: Session = Depends(get_db)):
    
    registro = db.query(Maestro).filter(Maestro.id == maestro_id).first()
    
    if not registro:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "mensaje": "Maestro no encontrado"}
        )

    # verificar si username ya existe en otro maestro
    usuario_existente = db.query(Maestro).filter(
        Maestro.username == maestro.username,
        Maestro.id != maestro_id
    ).first()

    if usuario_existente:
        return JSONResponse(
            status_code=200,
            content={"status": "error", "mensaje": "Usuario ya existe"}
        )

    # actualizar datos
    for k, v in maestro.model_dump(exclude_unset=True).items():
        setattr(registro, k, v)

    db.commit()

    return JSONResponse(
        status_code=200,
        content={"status": "ok", "mensaje": "Maestro editado correctamente"}
    )

# Eliminar maestro
@router.delete("/{maestro_id}")
def eliminar_maestro(maestro_id: int, db: Session = Depends(get_db)):
    registro = db.query(Maestro).filter(Maestro.id == maestro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Maestro no encontrado")

    db.delete(registro)
    db.commit()
    return {"mensaje": "Maestro eliminado"}
