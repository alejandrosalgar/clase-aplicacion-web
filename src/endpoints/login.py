from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.entities.usuarios import Usuario
from src.schemas.login_schema import Login
from src.utils.security import verify_password


router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/login")
def login(dato: Login, db: Session = Depends(get_db)):
    user = (
        db.query(Usuario).filter(Usuario.nombre_usuario == dato.nombre_usuario).first()
    )
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    if not verify_password(dato.contraseña, user.contraseña_hash):
        raise HTTPException(
            status_code=401, detail="Contraseña no válida para el usuario"
        )
    if user.rol.lower() != "admin":
        raise HTTPException(
            status_code=403, detail="Acceso restringido, el usuario no es administrador"
        )
    return {"resultado": "Login exitoso", "id_usuario": user.id_usuario}
