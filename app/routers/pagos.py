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

VALORES_PAQUETE = {
    1: 3150,
    2: 3350,
    3: 3550,
    4: 3750,
    5: 3950,
    6: 4200,
    7: 4750,
    8: 5000,
    9: 5300
}


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


@router.post("/registrar_salida/{nino_id}", response_model=PagoResponse)
def registrar_salida(nino_id: int, paquete: int, horas_totales: int, db: Session = Depends(get_db)):

    ahora = datetime.now()
    mes_actual = ahora.month
    anio_actual = ahora.year

    valor_paquete = VALORES_PAQUETE.get(paquete)
    if not valor_paquete:
        raise HTTPException(status_code=400, detail="Paquete inválido")

    horas_incluidas = paquete + 3
    horas_extra = max(0, horas_totales - horas_incluidas)
    costo_extra = horas_extra * 80

    pago_existente = db.query(Pago).filter(
        Pago.nino_id == nino_id,
        Pago.mes == mes_actual,
        Pago.anio == anio_actual
    ).first()

    if not pago_existente:
        nuevo_pago = Pago(
            nino_id=nino_id,
            mes=mes_actual,
            anio=anio_actual,
            deuda=valor_paquete + costo_extra,
            pago=0.0,
            estado=0
        )
        db.add(nuevo_pago)
        db.commit()
        db.refresh(nuevo_pago)
        return nuevo_pago
    else:
        if pago_existente.deuda < valor_paquete:
            pago_existente.deuda = valor_paquete

        if costo_extra > 0:
            pago_existente.deuda += costo_extra

        if pago_existente.pago >= pago_existente.deuda:
            pago_existente.estado = 1
        elif pago_existente.pago > 0:
            pago_existente.estado = 2
        else:
            pago_existente.estado = 0

        db.commit()
        db.refresh(pago_existente)
        return pago_existente