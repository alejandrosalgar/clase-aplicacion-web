from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.core.exceptions import NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.sucursal import Sucursal
from src.schemas.sucursal_schema import SucursalCreate, SucursalUpdate, SucursalResponse

router = APIRouter(
    prefix="/sucursales",
    tags=["sucursales"],
    dependencies=[Depends(get_current_user)],
)


@router.get("")
def listar_sucursales(db: Session = Depends(get_db)):
    sucursales = db.query(Sucursal).all()
    data = [
        SucursalResponse.model_validate(s).model_dump(mode="json") for s in sucursales
    ]
    return success_response(data=data, message="Listado de sucursales")


@router.get("/{sucursal_id}")
def obtener_sucursal(sucursal_id: UUID, db: Session = Depends(get_db)):
    sucursal = db.query(Sucursal).filter(Sucursal.id_sucursal == sucursal_id).first()
    if not sucursal:
        raise NotFoundError("Sucursal no encontrada")
    data = SucursalResponse.model_validate(sucursal).model_dump(mode="json")
    return success_response(data=data, message="Sucursal obtenida")


@router.post("", status_code=201)
def crear_sucursal(dato: SucursalCreate, db: Session = Depends(get_db)):
    sucursal = Sucursal(
        nombre=dato.nombre,
        direccion=dato.direccion,
        ciudad=dato.ciudad,
        telefono=dato.telefono,
        id_usuario_creacion=dato.id_usuario_creacion,
    )
    db.add(sucursal)
    db.commit()
    db.refresh(sucursal)
    data = SucursalResponse.model_validate(sucursal).model_dump(mode="json")
    return success_response(data=data, message="Sucursal creada")


@router.put("/{sucursal_id}")
def actualizar_sucursal(
    sucursal_id: UUID, dato: SucursalUpdate, db: Session = Depends(get_db)
):
    sucursal = db.query(Sucursal).filter(Sucursal.id_sucursal == sucursal_id).first()
    if not sucursal:
        raise NotFoundError("Sucursal no encontrada")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(sucursal, k, v)
    db.commit()
    db.refresh(sucursal)
    data = SucursalResponse.model_validate(sucursal).model_dump(mode="json")
    return success_response(data=data, message="Sucursal actualizada")


@router.delete("/{sucursal_id}", status_code=204)
def eliminar_sucursal(sucursal_id: UUID, db: Session = Depends(get_db)):
    sucursal = db.query(Sucursal).filter(Sucursal.id_sucursal == sucursal_id).first()
    if not sucursal:
        raise NotFoundError("Sucursal no encontrada")
    db.delete(sucursal)
    db.commit()
    return None
