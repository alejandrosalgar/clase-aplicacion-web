from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.tipo_prestamo import TipoPrestamo
from src.schemas.tipo_prestamo_schema import (
    TipoPrestamoCreate,
    TipoPrestamoUpdate,
    TipoPrestamoResponse,
)

router = APIRouter(prefix="/tipo_prestamo", tags=["tipo_prestamo"])


@router.get("")
def listar_tipos_prestamo(db: Session = Depends(get_db)):
    tipos = db.query(TipoPrestamo).all()
    data = [
        TipoPrestamoResponse.model_validate(t).model_dump(mode="json") for t in tipos
    ]
    return success_response(data=data, message="Lista de tipos de prestamo")


@router.get("/{id_tipo_prestamo}")
def obtener_tipo_prestamo(id_tipo_prestamo: UUID, db: Session = Depends(get_db)):
    tipo = (
        db.query(TipoPrestamo)
        .filter(TipoPrestamo.id_tipo_prestamo == id_tipo_prestamo)
        .first()
    )
    if not tipo:
        raise NotFoundError("Tipo de prestamo no encontrado")
    data = TipoPrestamoResponse.model_validate(tipo).model_dump(mode="json")
    return success_response(data=data, message="Tipo de prestamo obtenido")


@router.post("", status_code=201)
def crear_tipo_prestamo(dato: TipoPrestamoCreate, db: Session = Depends(get_db)):
    tipo = TipoPrestamo(
        nombre=dato.nombre,
        descripcion=dato.descripcion,
        estado=dato.estado,
        id_usuario_creacion=dato.id_usuario_creacion,
    )
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    data = TipoPrestamoResponse.model_validate(tipo).model_dump(mode="json")
    return success_response(data=data, message="Tipo de prestamo creado")


@router.put("/{id_tipo_prestamo}")
def actualizar_tipo_prestamo(
    id_tipo_prestamo: UUID,
    dato: TipoPrestamoUpdate,
    db: Session = Depends(get_db),
):
    tipo = (
        db.query(TipoPrestamo)
        .filter(TipoPrestamo.id_tipo_prestamo == id_tipo_prestamo)
        .first()
    )
    if not tipo:
        raise NotFoundError("Tipo de prestamo no encontrado")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(tipo, k, v)
    db.commit()
    db.refresh(tipo)
    data = TipoPrestamoResponse.model_validate(tipo).model_dump(mode="json")
    return success_response(data=data, message="Tipo de prestamo actualizado")


@router.delete("/{id_tipo_prestamo}", status_code=204)
def eliminar_tipo_prestamo(id_tipo_prestamo: UUID, db: Session = Depends(get_db)):
    tipo = (
        db.query(TipoPrestamo)
        .filter(TipoPrestamo.id_tipo_prestamo == id_tipo_prestamo)
        .first()
    )
    if not tipo:
        raise NotFoundError("Tipo de prestamo no encontrado")
    db.delete(tipo)
    db.commit()
    return None
