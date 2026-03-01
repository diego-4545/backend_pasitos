from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.security import verificar_api_key
from app.models.pago import Pago
from app.schemas.pago import PagoCreate, PagoUpdate, PagoResponse

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"],
    dependencies=[Depends(verificar_api_key)]
)


@router.post("/", response_model=PagoResponse)
def crear_pago(pago: PagoCreate, db: Session = Depends(get_db)):

    pago_existente = db.query(Pago).filter(
        Pago.nino_id == pago.nino_id,
        Pago.mes == pago.mes,
        Pago.anio == pago.anio
    ).first()

    if pago_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un pago para este niño en ese mes"
        )

    nuevo = Pago(**pago.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.get("/", response_model=list[PagoResponse])
def listar_pagos(db: Session = Depends(get_db)):
    return db.query(Pago).all()


@router.get("/nino/{nino_id}", response_model=list[PagoResponse])
def obtener_pagos_por_nino(nino_id: int, db: Session = Depends(get_db)):
    return db.query(Pago).filter(Pago.nino_id == nino_id).all()


@router.put("/{pago_id}", response_model=PagoResponse)
def actualizar_pago(pago_id: int, pago: PagoUpdate, db: Session = Depends(get_db)):

    registro = db.query(Pago).filter(Pago.id == pago_id).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    for k, v in pago.model_dump(exclude_unset=True).items():
        setattr(registro, k, v)

    if registro.pago >= registro.deuda:
        registro.estado = 1  
    elif registro.pago > 0:
        registro.estado = 2  
    else:
        registro.estado = 0  

    db.commit()
    db.refresh(registro)

    return registro