from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SucursalBase(BaseModel):
    nombre: str
    direccion: str | None = None
    ciudad: str | None = None
    telefono: str | None = None


class SucursalCreate(SucursalBase):
    id_usuario_creacion: UUID


class SucursalUpdate(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    ciudad: str | None = None
    telefono: str | None = None
    id_usuario_edita: UUID | None = None


class SucursalResponse(SucursalBase):
    id_sucursal: UUID
    id_usuario_creacion: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
