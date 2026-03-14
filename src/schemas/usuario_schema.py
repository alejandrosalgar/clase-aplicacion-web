from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    telefono: str | None = None
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    contraseña: str
    rol: str


class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    nombre_usuario: str | None = None
    email: EmailStr | None = None
    contraseña: str | None = None
    telefono: str | None = None
    rol: str | None = None
    activo: bool | None = None


class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    rol: str
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
