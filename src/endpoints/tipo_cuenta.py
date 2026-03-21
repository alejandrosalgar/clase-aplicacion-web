from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.tipo_cuenta import TipoCuenta
from src.schemas.tipo_cuenta_schema import (
    TipoCuentaCreate,
    TipoCuentaUpdate,
    TipoCuentaResponse,
)

router = APIRouter(prefix="/tipos-cuenta", tags=["tipos-cuenta"])


@router.get("")
def listar_tipos_cuenta(db: Session = Depends(get_db)):
    tipos = db.query(TipoCuenta).all()
    data = [TipoCuentaResponse.model_validate(t).model_dump(mode="json") for t in tipos]
    return success_response(data=data, message="Listado de tipos de cuenta")


@router.get("/{tipo_id}")
def obtener_tipo_cuenta(tipo_id: UUID, db: Session = Depends(get_db)):
    tipo = db.query(TipoCuenta).filter(TipoCuenta.id_tipo_cuenta == tipo_id).first()
    if not tipo:
        raise NotFoundError("Tipo de cuenta no encontrado")
    data = TipoCuentaResponse.model_validate(tipo).model_dump(mode="json")
    return success_response(data=data, message="Tipo de cuenta obtenido")


@router.post("", status_code=201)
def crear_tipo_cuenta(dato: TipoCuentaCreate, db: Session = Depends(get_db)):
    if db.query(TipoCuenta).filter(TipoCuenta.codigo == dato.codigo).first():
        raise ConflictError("Ya existe un tipo de cuenta con ese código", status_code=400)
    tipo = TipoCuenta(
        codigo=dato.codigo,
        nombre=dato.nombre,
        id_usuario_creacion=dato.id_usuario_creacion,
    )
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    data = TipoCuentaResponse.model_validate(tipo).model_dump(mode="json")
    return success_response(data=data, message="Tipo de cuenta creado")


@router.put("/{tipo_id}")
def actualizar_tipo_cuenta(
    tipo_id: UUID, dato: TipoCuentaUpdate, db: Session = Depends(get_db)
):
    tipo = db.query(TipoCuenta).filter(TipoCuenta.id_tipo_cuenta == tipo_id).first()
    if not tipo:
        raise NotFoundError("Tipo de cuenta no encontrado")
    update = dato.model_dump(exclude_unset=True)
    if (
        "codigo" in update
        and db.query(TipoCuenta)
        .filter(
            TipoCuenta.codigo == update["codigo"], TipoCuenta.id_tipo_cuenta != tipo_id
        )
        .first()
    ):
        raise ConflictError("El código ya existe", status_code=400)
    for k, v in update.items():
        setattr(tipo, k, v)
    db.commit()
    db.refresh(tipo)
    data = TipoCuentaResponse.model_validate(tipo).model_dump(mode="json")
    return success_response(data=data, message="Tipo de cuenta actualizado")


@router.delete("/{tipo_id}", status_code=204)
def eliminar_tipo_cuenta(tipo_id: UUID, db: Session = Depends(get_db)):
    tipo = db.query(TipoCuenta).filter(TipoCuenta.id_tipo_cuenta == tipo_id).first()
    if not tipo:
        raise NotFoundError("Tipo de cuenta no encontrado")
    db.delete(tipo)
    db.commit()
    return None
