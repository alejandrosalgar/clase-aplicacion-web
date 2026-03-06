from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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


@router.get("", response_model=list[TransaccionResponse])
def listar_transacciones(db: Session = Depends(get_db)):
    return db.query(Transaccion).all()


@router.get("/{transaccion_id}", response_model=TransaccionResponse)
def obtener_transaccion(transaccion_id: UUID, db: Session = Depends(get_db)):
    t = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return t


@router.post("", response_model=TransaccionResponse, status_code=201)
def crear_transaccion(dato: TransaccionCreate, db: Session = Depends(get_db)):
    if not db.query(Cuenta).filter(Cuenta.id == dato.id_cuenta).first():
        raise HTTPException(status_code=400, detail="Cuenta no encontrada")
    if not db.query(TipoTransaccion).filter(
        TipoTransaccion.id == dato.id_tipo_transaccion
    ).first():
        raise HTTPException(status_code=400, detail="Tipo de transacción no encontrado")
    if dato.id_cuenta_destino and not db.query(Cuenta).filter(
        Cuenta.id == dato.id_cuenta_destino
    ).first():
        raise HTTPException(status_code=400, detail="Cuenta destino no encontrada")
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
    return t


@router.put("/{transaccion_id}", response_model=TransaccionResponse)
def actualizar_transaccion(
    transaccion_id: UUID, dato: TransaccionUpdate, db: Session = Depends(get_db)
):
    t = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{transaccion_id}", status_code=204)
def eliminar_transaccion(transaccion_id: UUID, db: Session = Depends(get_db)):
    t = db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    db.delete(t)
    db.commit()
    return None
