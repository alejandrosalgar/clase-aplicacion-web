from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.tipo_transaccion import TipoTransaccion
from src.schemas.tipo_transaccion_schema import (
    TipoTransaccionCreate,
    TipoTransaccionUpdate,
    TipoTransaccionResponse,
)

router = APIRouter(prefix="/tipos-transaccion", tags=["tipos-transaccion"])


@router.get("", response_model=list[TipoTransaccionResponse])
def listar_tipos_transaccion(db: Session = Depends(get_db)):
    return db.query(TipoTransaccion).all()


@router.get("/{tipo_id}", response_model=TipoTransaccionResponse)
def obtener_tipo_transaccion(tipo_id: UUID, db: Session = Depends(get_db)):
    tipo = (
        db.query(TipoTransaccion)
        .filter(TipoTransaccion.id_tipo_transaccion == tipo_id)
        .first()
    )
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de transacción no encontrado")
    return tipo


@router.post("", response_model=TipoTransaccionResponse, status_code=201)
def crear_tipo_transaccion(dato: TipoTransaccionCreate, db: Session = Depends(get_db)):
    if db.query(TipoTransaccion).filter(TipoTransaccion.codigo == dato.codigo).first():
        raise HTTPException(
            status_code=400, detail="Ya existe un tipo de transacción con ese código"
        )
    tipo = TipoTransaccion(
        codigo=dato.codigo,
        nombre=dato.nombre,
        id_usuario_creacion=dato.id_usuario_creacion,
    )
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo


@router.put("/{tipo_id}", response_model=TipoTransaccionResponse)
def actualizar_tipo_transaccion(
    tipo_id: UUID, dato: TipoTransaccionUpdate, db: Session = Depends(get_db)
):
    tipo = (
        db.query(TipoTransaccion)
        .filter(TipoTransaccion.id_tipo_transaccion == tipo_id)
        .first()
    )
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de transacción no encontrado")
    update = dato.model_dump(exclude_unset=True)
    if (
        "codigo" in update
        and db.query(TipoTransaccion)
        .filter(
            TipoTransaccion.codigo == update["codigo"],
            TipoTransaccion.id_tipo_transaccion != tipo_id,
        )
        .first()
    ):
        raise HTTPException(status_code=400, detail="El código ya existe")
    for k, v in update.items():
        setattr(tipo, k, v)
    db.commit()
    db.refresh(tipo)
    return tipo


@router.delete("/{tipo_id}", status_code=204)
def eliminar_tipo_transaccion(tipo_id: UUID, db: Session = Depends(get_db)):
    tipo = (
        db.query(TipoTransaccion)
        .filter(TipoTransaccion.id_tipo_transaccion == tipo_id)
        .first()
    )
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de transacción no encontrado")
    db.delete(tipo)
    db.commit()
    return None
