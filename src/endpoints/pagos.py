from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.pagos import Pago
from src.schemas.pagos_schema import PagoCreate, PagoUpdate, PagoResponse

router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("")
def listar_pagos(db: Session = Depends(get_db)):
    pagos = db.query(Pago).all()
    data = [PagoResponse.model_validate(p).model_dump(mode="json") for p in pagos]
    return success_response(data=data, message="Lista de pagos")


@router.get("/{id_pago}")
def obtener_pago(id_pago: UUID, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise NotFoundError("Pago no encontrado")
    data = PagoResponse.model_validate(pago).model_dump(mode="json")
    return success_response(data=data, message="Pago obtenido")


@router.post("", status_code=201)
def crear_pago(dato: PagoCreate, db: Session = Depends(get_db)):
    pago = Pago(
        monto=dato.monto,
        id_prestamo=dato.id_prestamo,
        estado=dato.estado,
        id_usuario_creacion=dato.id_usuario_creacion,
    )
    db.add(pago)
    db.commit()
    db.refresh(pago)
    data = PagoResponse.model_validate(pago).model_dump(mode="json")
    return success_response(data=data, message="Pago creado")


@router.put("/{id_pago}")
def actualizar_pago(id_pago: UUID, dato: PagoUpdate, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise NotFoundError("Pago no encontrado")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(pago, k, v)
    db.commit()
    db.refresh(pago)
    data = PagoResponse.model_validate(pago).model_dump(mode="json")
    return success_response(data=data, message="Pago actualizado")


@router.delete("/{id_pago}", status_code=204)
def eliminar_pago(id_pago: UUID, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id_pago == id_pago).first()
    if not pago:
        raise NotFoundError("Pago no encontrado")
    db.delete(pago)
    db.commit()
    return None
