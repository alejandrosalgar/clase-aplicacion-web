from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.prestamo import Prestamo
from src.schemas.prestamo_schema import PrestamoCreate, PrestamoUpdate, PrestamoResponse

router = APIRouter(prefix= "/prestamos", tags = ["prestamos"])

@router.get("")
def listar_prestamos(db: Session = Depends(get_db)):
    prestamos = db.query(Prestamo).all()
    data = [PrestamoResponse.model_validate(p).model_dump(mode="json") for p in prestamos]
    return success_response(data=data, message="Lista de prestamos")

@router.get("/{id_prestamo}")
def obtener_prestamo(id_prestamo: UUID, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.id_prestamo == id_prestamo).first()
    if not prestamo:
        raise NotFoundError("Prestamo no econtrado")
    data = PrestamoResponse.model_validate(prestamo).model_dump(mode="json")
    return success_response(data=data, message="Prestamo obtenido")

@router.post("", status_code=201)
def crear_prestamo(dato: PrestamoCreate, db: Session = Depends(get_db)):
    prestamo = Prestamo(
        valor=dato.valor,
        valor_pendiente=dato.valor,
        interes=dato.interes,
        plazo=dato.plazo,
        id_usuario=dato.id_usuario,
        estado=dato.estado,
        id_usuario_creacion=dato.id_usuario_creacion,
    )
    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    data = PrestamoResponse.model_validate(prestamo).model_dump(mode="json")
    return success_response(data=data, message="Prestamo creado")

@router.put("/{id_prestamo}")
def actualizar_prestamo(
    id_prestamo: UUID, dato: PrestamoUpdate, db: Session = Depends(get_db)
):
    prestamo = db.query(Prestamo).filter(Prestamo.id_prestamo == id_prestamo).first()
    if not prestamo:
        raise NotFoundError("Prestamo no encontrado")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(prestamo, k, v)
    db.commit()
    db.refresh(prestamo)
    data = PrestamoResponse.model_validate(prestamo).model_dump(mode="json")
    return success_response(data=data, message="Prestamo actualizado")

@router.delete("/{id_prestamo}", status_code=204)
def eliminar_sucursal(id_prestamo: UUID, db: Session = Depends(get_db)):
    prestamo = db.query(Prestamo).filter(Prestamo.id_prestamo == id_prestamo).first()
    if not prestamo:
        raise NotFoundError("Prestamo no encontrado")
    db.delete(Prestamo)
    db.commit()
    return None