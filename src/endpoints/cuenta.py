from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.cuenta import Cuenta
from src.entities.sucursal import Sucursal
from src.entities.tipo_cuenta import TipoCuenta
from src.entities.usuarios import Usuario
from src.schemas.cuenta_schema import CuentaCreate, CuentaUpdate, CuentaResponse

router = APIRouter(prefix="/cuentas", tags=["cuentas"])


@router.get("", response_model=list[CuentaResponse])
def listar_cuentas(db: Session = Depends(get_db)):
    return db.query(Cuenta).all()


@router.get("/{cuenta_id}", response_model=CuentaResponse)
def obtener_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return cuenta


@router.post("", response_model=CuentaResponse, status_code=201)
def crear_cuenta(dato: CuentaCreate, db: Session = Depends(get_db)):
    if db.query(Cuenta).filter(Cuenta.numero_cuenta == dato.numero_cuenta).first():
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese número")
    if not db.query(Usuario).filter(Usuario.id == dato.id_usuario).first():
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    if not db.query(Sucursal).filter(Sucursal.id == dato.id_sucursal).first():
        raise HTTPException(status_code=400, detail="Sucursal no encontrada")
    if not db.query(TipoCuenta).filter(TipoCuenta.id == dato.id_tipo_cuenta).first():
        raise HTTPException(status_code=400, detail="Tipo de cuenta no encontrado")
    saldo = dato.saldo if dato.saldo is not None else 0
    cuenta = Cuenta(
        numero_cuenta=dato.numero_cuenta,
        id_usuario=dato.id_usuario,
        id_sucursal=dato.id_sucursal,
        id_tipo_cuenta=dato.id_tipo_cuenta,
        saldo=saldo,
    )
    db.add(cuenta)
    db.commit()
    db.refresh(cuenta)
    return cuenta


@router.put("/{cuenta_id}", response_model=CuentaResponse)
def actualizar_cuenta(
    cuenta_id: UUID, dato: CuentaUpdate, db: Session = Depends(get_db)
):
    cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    update = dato.model_dump(exclude_unset=True)
    if "numero_cuenta" in update:
        if db.query(Cuenta).filter(
            Cuenta.numero_cuenta == update["numero_cuenta"], Cuenta.id != cuenta_id
        ).first():
            raise HTTPException(status_code=400, detail="Número de cuenta ya existe")
    if "id_sucursal" in update and not db.query(Sucursal).filter(
        Sucursal.id == update["id_sucursal"]
    ).first():
        raise HTTPException(status_code=400, detail="Sucursal no encontrada")
    if "id_tipo_cuenta" in update and not db.query(TipoCuenta).filter(
        TipoCuenta.id == update["id_tipo_cuenta"]
    ).first():
        raise HTTPException(status_code=400, detail="Tipo de cuenta no encontrado")
    for k, v in update.items():
        setattr(cuenta, k, v)
    db.commit()
    db.refresh(cuenta)
    return cuenta


@router.delete("/{cuenta_id}", status_code=204)
def eliminar_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    db.delete(cuenta)
    db.commit()
    return None
