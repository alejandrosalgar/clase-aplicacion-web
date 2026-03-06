from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SucursalBase(BaseModel):
    nombre: str
    direccion: str | None = None
    ciudad: str | None = None
    telefono: str | None = None


class SucursalCreate(SucursalBase):
    pass


class SucursalUpdate(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    ciudad: str | None = None
    telefono: str | None = None


class SucursalResponse(SucursalBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
