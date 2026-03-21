from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SucursalBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200, description="Nombre de la sucursal")
    direccion: str | None = Field(None, max_length=300)
    ciudad: str | None = Field(None, max_length=100)
    telefono: str | None = Field(None, max_length=20)


class SucursalCreate(SucursalBase):
    id_usuario_creacion: UUID


class SucursalUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=200)
    direccion: str | None = Field(None, max_length=300)
    ciudad: str | None = Field(None, max_length=100)
    telefono: str | None = Field(None, max_length=20)
    id_usuario_edita: UUID | None = None


class SucursalResponse(SucursalBase):
    id_sucursal: UUID
    id_usuario_creacion: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
