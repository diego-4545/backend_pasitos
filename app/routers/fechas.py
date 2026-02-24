from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exists, and_, not_
from datetime import datetime, timezone
from typing import Optional

from app.database import get_db
from app.security import verificar_api_key
from app.models.fecha import Fecha
from app.models.nino import Nino
from app.schemas.fecha import FechaCreate, FechaUpdate 

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


# --- Endpoint para obtener niños SIN fechas activas en una sucursal ---
@router.get("/disponibles/{sucursal_id}")
def obtener_ninos_disponibles(sucursal_id: int, db: Session = Depends(get_db)):
    """
    Devuelve los Nino de la sucursal que NO tienen una fecha activa ahora.
    Activa = hora_inicio <= ahora <= hora_fin
    """
    ahora = datetime.now(timezone.utc)  # o datetime.now() si no usas tz; ajusta según tu base
    
    # Subconsulta: existe alguna fecha activa para ese niño?
    subquery = db.query(Fecha).filter(
        and_(
            Fecha.nino_id == Nino.id,
            Fecha.hora_inicio <= ahora,
            Fecha.hora_fin >= ahora
        )
    )
    
    # Seleccionamos los niños de la sucursal donde NO exista fecha activa
    ninos = db.query(Nino).filter(
        Nino.sucursal == sucursal_id,
        not_(exists(subquery))
    ).all()

    return ninos


# --- PUT para actualizar una fecha por id ---
@router.put("/{fecha_id}")
def actualizar_fecha(fecha_id: int, fecha_update: "FechaUpdate", db: Session = Depends(get_db)):
    """
    Actualiza los campos enviados de una Fecha (solo los que envíes).
    FechaUpdate debe ser un schema Pydantic con campos opcionales.
    """
    db_fecha = db.query(Fecha).filter(Fecha.id == fecha_id).first()
    if not db_fecha:
        raise HTTPException(status_code=404, detail="Fecha no encontrada")

    # Usando Pydantic v2: model_dump(exclude_unset=True)
    cambios = fecha_update.model_dump(exclude_unset=True)
    for key, val in cambios.items():
        setattr(db_fecha, key, val)

    db.add(db_fecha)
    db.commit()
    db.refresh(db_fecha)
    return db_fecha