from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.tipo_transaccion import TipoTransaccion
from src.schemas.tipo_transaccion_schema import (
    TipoTransaccionCreate,
    TipoTransaccionUpdate,
    TipoTransaccionResponse,
)

router = APIRouter(prefix="/tipos-transaccion", tags=["tipos-transaccion"])


@router.get("")
def listar_tipos_transaccion(db: Session = Depends(get_db)):
    tipos = db.query(TipoTransaccion).all()
    data = [TipoTransaccionResponse.model_validate(t).model_dump(mode="json") for t in tipos]
    return success_response(data=data, message="Listado de tipos de transacción")


@router.get("/{tipo_id}")
def obtener_tipo_transaccion(tipo_id: UUID, db: Session = Depends(get_db)):
    tipo = (
        db.query(TipoTransaccion)
        .filter(TipoTransaccion.id_tipo_transaccion == tipo_id)
        .first()
    )
    if not tipo:
        raise NotFoundError("Tipo de transacción no encontrado")
    data = TipoTransaccionResponse.model_validate(tipo).model_dump(mode="json")
    return success_response(data=data, message="Tipo de transacción obtenido")


@router.post("", status_code=201)
def crear_tipo_transaccion(dato: TipoTransaccionCreate, db: Session = Depends(get_db)):
    if db.query(TipoTransaccion).filter(TipoTransaccion.codigo == dato.codigo).first():
        raise ConflictError(
            "Ya existe un tipo de transacción con ese código", status_code=400
        )
    tipo = TipoTransaccion(
        codigo=dato.codigo,
        nombre=dato.nombre,
        id_usuario_creacion=dato.id_usuario_creacion,
    )
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    data = TipoTransaccionResponse.model_validate(tipo).model_dump(mode="json")
    return success_response(data=data, message="Tipo de transacción creado")


@router.put("/{tipo_id}")
def actualizar_tipo_transaccion(
    tipo_id: UUID, dato: TipoTransaccionUpdate, db: Session = Depends(get_db)
):
    tipo = (
        db.query(TipoTransaccion)
        .filter(TipoTransaccion.id_tipo_transaccion == tipo_id)
        .first()
    )
    if not tipo:
        raise NotFoundError("Tipo de transacción no encontrado")
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
        raise ConflictError("El código ya existe", status_code=400)
    for k, v in update.items():
        setattr(tipo, k, v)
    db.commit()
    db.refresh(tipo)
    data = TipoTransaccionResponse.model_validate(tipo).model_dump(mode="json")
    return success_response(data=data, message="Tipo de transacción actualizado")


@router.delete("/{tipo_id}", status_code=204)
def eliminar_tipo_transaccion(tipo_id: UUID, db: Session = Depends(get_db)):
    tipo = (
        db.query(TipoTransaccion)
        .filter(TipoTransaccion.id_tipo_transaccion == tipo_id)
        .first()
    )
    if not tipo:
        raise NotFoundError("Tipo de transacción no encontrado")
    db.delete(tipo)
    db.commit()
    return None
