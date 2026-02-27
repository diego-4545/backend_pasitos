from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exists, and_, not_
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import and_, or_, not_, exists
from app.database import get_db
from app.security import verificar_api_key
from app.models.fecha import Fecha
from app.models.nino import Nino
from app.schemas.fecha import FechaCreate, FechaUpdate 
from sqlalchemy import and_, exists, not_

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

    subquery = exists().where(
        and_(
            Fecha.nino_id == Nino.id,
            Fecha.hora_inicio != None,
            Fecha.hora_fin == None   # sigue dentro
        )
    )

    ninos = db.query(Nino).filter(
        Nino.sucursal == sucursal_id,
        not_(subquery)  # que NO tenga una fecha abierta
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


@router.get("/fechas/abiertas/{sucursal_id}")
def obtener_fechas_abiertas(sucursal_id: int, db: Session = Depends(get_db)):
    """
    Devuelve todas las fechas sin hora_fin
    de los niños de una sucursal específica
    """

    fechas = (
        db.query(Fecha)
        .join(Nino, Fecha.nino_id == Nino.id)
        .filter(
            Nino.sucursal == sucursal_id,
            Fecha.hora_inicio != None,
            Fecha.hora_fin == None
        )
        .all()
    )

    return fechas