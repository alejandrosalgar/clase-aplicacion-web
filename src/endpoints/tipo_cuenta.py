from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.tipo_cuenta import TipoCuenta
from src.schemas.tipo_cuenta_schema import (
    TipoCuentaCreate,
    TipoCuentaUpdate,
    TipoCuentaResponse,
)

router = APIRouter(prefix="/tipos-cuenta", tags=["tipos-cuenta"])


@router.get("", response_model=list[TipoCuentaResponse])
def listar_tipos_cuenta(db: Session = Depends(get_db)):
    return db.query(TipoCuenta).all()


@router.get("/{tipo_id}", response_model=TipoCuentaResponse)
def obtener_tipo_cuenta(tipo_id: UUID, db: Session = Depends(get_db)):
    tipo = db.query(TipoCuenta).filter(TipoCuenta.id_tipo_cuenta == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    return tipo


@router.post("", response_model=TipoCuentaResponse, status_code=201)
def crear_tipo_cuenta(dato: TipoCuentaCreate, db: Session = Depends(get_db)):
    if db.query(TipoCuenta).filter(TipoCuenta.codigo == dato.codigo).first():
        raise HTTPException(
            status_code=400, detail="Ya existe un tipo de cuenta con ese código"
        )
    tipo = TipoCuenta(
        codigo=dato.codigo,
        nombre=dato.nombre,
        id_usuario_creacion=dato.id_usuario_creacion,
    )
    db.add(tipo)
    db.commit()
    db.refresh(tipo)
    return tipo


@router.put("/{tipo_id}", response_model=TipoCuentaResponse)
def actualizar_tipo_cuenta(
    tipo_id: UUID, dato: TipoCuentaUpdate, db: Session = Depends(get_db)
):
    tipo = db.query(TipoCuenta).filter(TipoCuenta.id_tipo_cuenta == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    update = dato.model_dump(exclude_unset=True)
    if (
        "codigo" in update
        and db.query(TipoCuenta)
        .filter(
            TipoCuenta.codigo == update["codigo"], TipoCuenta.id_tipo_cuenta != tipo_id
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
def eliminar_tipo_cuenta(tipo_id: UUID, db: Session = Depends(get_db)):
    tipo = db.query(TipoCuenta).filter(TipoCuenta.id_tipo_cuenta == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de cuenta no encontrado")
    db.delete(tipo)
    db.commit()
    return None
