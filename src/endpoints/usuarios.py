from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.usuarios import Usuario
from src.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from src.utils.security import hash_password

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("", response_model=UsuarioResponse, status_code=201)
def crear_usuario(dato: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.nombre_usuario == dato.nombre_usuario).first():
        raise HTTPException(status_code=400, detail="Nombre de usuario ya existe")
    if db.query(Usuario).filter(Usuario.email == dato.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    usuario = Usuario(
        nombre=dato.nombre,
        nombre_usuario=dato.nombre_usuario,
        email=dato.email,
        contraseña_hash=hash_password(dato.contraseña),
        telefono=dato.telefono,
        activo=dato.activo,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: UUID, dato: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    update = dato.model_dump(exclude_unset=True)
    if "contraseña" in update and update["contraseña"]:
        update["contraseña_hash"] = hash_password(update.pop("contraseña"))
    for k, v in update.items():
        setattr(usuario, k, v)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return None
