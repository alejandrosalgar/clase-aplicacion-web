from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import BadRequestError, NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.cuenta import Cuenta
from src.entities.transaccion import Transaccion
from src.entities.tipo_transaccion import TipoTransaccion
from src.schemas.transaccion_schema import (
    TransaccionCreate,
    TransaccionUpdate,
    TransaccionResponse,
)

router = APIRouter(prefix="/transacciones", tags=["transacciones"])


@router.get("")
def listar_transacciones(db: Session = Depends(get_db)):
    transacciones = db.query(Transaccion).all()
    data = [TransaccionResponse.model_validate(t).model_dump(mode="json") for t in transacciones]
    return success_response(data=data, message="Listado de transacciones")


@router.get("/{transaccion_id}")
def obtener_transaccion(transaccion_id: UUID, db: Session = Depends(get_db)):
    t = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not t:
        raise NotFoundError("Transacción no encontrada")
    data = TransaccionResponse.model_validate(t).model_dump(mode="json")
    return success_response(data=data, message="Transacción obtenida")


@router.post("", status_code=201)
def crear_transaccion(dato: TransaccionCreate, db: Session = Depends(get_db)):
    if not db.query(Cuenta).filter(Cuenta.id == dato.id_cuenta).first():
        raise BadRequestError("Cuenta no encontrada")
    if not db.query(TipoTransaccion).filter(
        TipoTransaccion.id == dato.id_tipo_transaccion
    ).first():
        raise BadRequestError("Tipo de transacción no encontrado")
    if dato.id_cuenta_destino and not db.query(Cuenta).filter(
        Cuenta.id == dato.id_cuenta_destino
    ).first():
        raise BadRequestError("Cuenta destino no encontrada")
    t = Transaccion(
        id_cuenta=dato.id_cuenta,
        id_tipo_transaccion=dato.id_tipo_transaccion,
        monto=dato.monto,
        id_cuenta_destino=dato.id_cuenta_destino,
        descripcion=dato.descripcion,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    data = TransaccionResponse.model_validate(t).model_dump(mode="json")
    return success_response(data=data, message="Transacción creada")


@router.put("/{transaccion_id}")
def actualizar_transaccion(
    transaccion_id: UUID, dato: TransaccionUpdate, db: Session = Depends(get_db)
):
    t = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not t:
        raise NotFoundError("Transacción no encontrada")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)
    data = TransaccionResponse.model_validate(t).model_dump(mode="json")
    return success_response(data=data, message="Transacción actualizada")


@router.delete("/{transaccion_id}", status_code=204)
def eliminar_transaccion(transaccion_id: UUID, db: Session = Depends(get_db)):
    t = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not t:
        raise NotFoundError("Transacción no encontrada")
    db.delete(t)
    db.commit()
    return None
