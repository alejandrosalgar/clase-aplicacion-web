from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.auth import get_current_user
from src.core.exceptions import ConflictError, NotFoundError
from src.core.responses import success_response
from src.database.config import get_db
from src.entities.usuarios import Usuario
from src.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from src.utils.security import hash_password

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", dependencies=[Depends(get_current_user)])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    data = [UsuarioResponse.model_validate(u).model_dump(mode="json") for u in usuarios]
    return success_response(data=data, message="Listado de usuarios")


@router.get("/{usuario_id}", dependencies=[Depends(get_current_user)])
def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        raise NotFoundError("Usuario no encontrado")
    data = UsuarioResponse.model_validate(usuario).model_dump(mode="json")
    return success_response(data=data, message="Usuario obtenido")


@router.post("", status_code=201)
def crear_usuario(dato: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.nombre_usuario == dato.nombre_usuario).first():
        raise ConflictError("Nombre de usuario ya existe", status_code=400)
    if db.query(Usuario).filter(Usuario.email == dato.email).first():
        raise ConflictError("Email ya registrado", status_code=400)
    usuario = Usuario(
        nombre=dato.nombre,
        nombre_usuario=dato.nombre_usuario,
        email=dato.email,
        contraseña_hash=hash_password(dato.contraseña),
        telefono=dato.telefono,
        activo=dato.activo,
        rol=dato.rol,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    data = UsuarioResponse.model_validate(usuario).model_dump(mode="json")
    return success_response(data=data, message="Usuario creado")


@router.put("/{usuario_id}", dependencies=[Depends(get_current_user)])
def actualizar_usuario(
    usuario_id: UUID, dato: UsuarioUpdate, db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        raise NotFoundError("Usuario no encontrado")
    update = dato.model_dump(exclude_unset=True)
    if "contraseña" in update and update["contraseña"]:
        update["contraseña_hash"] = hash_password(update.pop("contraseña"))
    for k, v in update.items():
        setattr(usuario, k, v)
    db.commit()
    db.refresh(usuario)
    data = UsuarioResponse.model_validate(usuario).model_dump(mode="json")
    return success_response(data=data, message="Usuario actualizado")


@router.delete(
    "/{usuario_id}", status_code=204, dependencies=[Depends(get_current_user)]
)
def eliminar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if not usuario:
        raise NotFoundError("Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return None
