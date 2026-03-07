from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.exceptions import BadRequestError, ConflictError, NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.cuenta import Cuenta
from src.entities.sucursal import Sucursal
from src.entities.tipo_cuenta import TipoCuenta
from src.entities.usuarios import Usuario
from src.schemas.cuenta_schema import CuentaCreate, CuentaUpdate, CuentaResponse

router = APIRouter(prefix="/cuentas", tags=["cuentas"])


@router.get("")
def listar_cuentas(db: Session = Depends(get_db)):
    cuentas = db.query(Cuenta).all()
    data = [CuentaResponse.model_validate(c).model_dump(mode="json") for c in cuentas]
    return success_response(data=data, message="Listado de cuentas")


@router.get("/{cuenta_id}")
def obtener_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
    if not cuenta:
        raise NotFoundError("Cuenta no encontrada")
    data = CuentaResponse.model_validate(cuenta).model_dump(mode="json")
    return success_response(data=data, message="Cuenta obtenida")


@router.post("", status_code=201)
def crear_cuenta(dato: CuentaCreate, db: Session = Depends(get_db)):
    if db.query(Cuenta).filter(Cuenta.numero_cuenta == dato.numero_cuenta).first():
        raise ConflictError("Ya existe una cuenta con ese número", status_code=400)
    if not db.query(Usuario).filter(Usuario.id == dato.id_usuario).first():
        raise BadRequestError("Usuario no encontrado")
    if not db.query(Sucursal).filter(Sucursal.id == dato.id_sucursal).first():
        raise BadRequestError("Sucursal no encontrada")
    if not db.query(TipoCuenta).filter(TipoCuenta.id == dato.id_tipo_cuenta).first():
        raise BadRequestError("Tipo de cuenta no encontrado")
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
    data = CuentaResponse.model_validate(cuenta).model_dump(mode="json")
    return success_response(data=data, message="Cuenta creada")


@router.put("/{cuenta_id}")
def actualizar_cuenta(
    cuenta_id: UUID, dato: CuentaUpdate, db: Session = Depends(get_db)
):
    cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
    if not cuenta:
        raise NotFoundError("Cuenta no encontrada")
    update = dato.model_dump(exclude_unset=True)
    if "numero_cuenta" in update:
        if db.query(Cuenta).filter(
            Cuenta.numero_cuenta == update["numero_cuenta"], Cuenta.id != cuenta_id
        ).first():
            raise ConflictError("Número de cuenta ya existe", status_code=400)
    if "id_sucursal" in update and not db.query(Sucursal).filter(
        Sucursal.id == update["id_sucursal"]
    ).first():
        raise BadRequestError("Sucursal no encontrada")
    if "id_tipo_cuenta" in update and not db.query(TipoCuenta).filter(
        TipoCuenta.id == update["id_tipo_cuenta"]
    ).first():
        raise BadRequestError("Tipo de cuenta no encontrado")
    for k, v in update.items():
        setattr(cuenta, k, v)
    db.commit()
    db.refresh(cuenta)
    data = CuentaResponse.model_validate(cuenta).model_dump(mode="json")
    return success_response(data=data, message="Cuenta actualizada")


@router.delete("/{cuenta_id}", status_code=204)
def eliminar_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    cuenta = db.query(Cuenta).filter(Cuenta.id == cuenta_id).first()
    if not cuenta:
        raise NotFoundError("Cuenta no encontrada")
    db.delete(cuenta)
    db.commit()
    return None
