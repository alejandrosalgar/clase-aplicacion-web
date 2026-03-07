from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200, description="Nombre completo")
    nombre_usuario: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Nombre de usuario único",
    )
    email: EmailStr
    telefono: str | None = Field(None, max_length=20)
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    contraseña: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Contraseña (mínimo 8 caracteres)",
    )

    @field_validator("contraseña")
    @classmethod
    def contraseña_no_vacia(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La contraseña no puede estar vacía")
        return v


class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=200)
    nombre_usuario: str | None = Field(
        None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.-]+$",
    )
    email: EmailStr | None = None
    contraseña: str | None = Field(None, min_length=8, max_length=100)
    telefono: str | None = Field(None, max_length=20)
    activo: bool | None = None


class UsuarioResponse(UsuarioBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
