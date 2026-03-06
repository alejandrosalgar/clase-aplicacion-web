from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.sucursal import Sucursal
from src.schemas.sucursal_schema import SucursalCreate, SucursalUpdate, SucursalResponse

router = APIRouter(prefix="/sucursales", tags=["sucursales"])


@router.get("", response_model=list[SucursalResponse])
def listar_sucursales(db: Session = Depends(get_db)):
    return db.query(Sucursal).all()


@router.get("/{sucursal_id}", response_model=SucursalResponse)
def obtener_sucursal(sucursal_id: UUID, db: Session = Depends(get_db)):
    sucursal = db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal


@router.post("", response_model=SucursalResponse, status_code=201)
def crear_sucursal(dato: SucursalCreate, db: Session = Depends(get_db)):
    sucursal = Sucursal(
        nombre=dato.nombre,
        direccion=dato.direccion,
        ciudad=dato.ciudad,
        telefono=dato.telefono,
    )
    db.add(sucursal)
    db.commit()
    db.refresh(sucursal)
    return sucursal


@router.put("/{sucursal_id}", response_model=SucursalResponse)
def actualizar_sucursal(
    sucursal_id: UUID, dato: SucursalUpdate, db: Session = Depends(get_db)
):
    sucursal = db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    update = dato.model_dump(exclude_unset=True)
    for k, v in update.items():
        setattr(sucursal, k, v)
    db.commit()
    db.refresh(sucursal)
    return sucursal


@router.delete("/{sucursal_id}", status_code=204)
def eliminar_sucursal(sucursal_id: UUID, db: Session = Depends(get_db)):
    sucursal = db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    db.delete(sucursal)
    db.commit()
    return None
