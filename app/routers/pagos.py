from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import verificar_api_key
from app.models.pago import Pago
from app.schemas.pago import PagoCreate, PagoUpdate

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"],
    dependencies=[Depends(verificar_api_key)]
)

@router.post("/")
def crear_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    nuevo = Pago(**pago.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/")
def listar_pagos(db: Session = Depends(get_db)):
    return db.query(Pago).all()

@router.put("/{pago_id}")
def actualizar_pago(pago_id: int, pago: PagoUpdate, db: Session = Depends(get_db)):
    registro = db.query(Pago).filter(Pago.id == pago_id).first()
    if not registro:
        raise HTTPException(404, "Pago no encontrado")

    for k, v in pago.model_dump(exclude_unset=True).items():
        setattr(registro, k, v)

    db.commit()
    return registro
