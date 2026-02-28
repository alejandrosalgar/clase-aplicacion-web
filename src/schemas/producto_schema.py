from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ProductoBase(BaseModel):
    nombre: str
    descripcion: str | None = None


class ProductoCreate(ProductoBase):
    id_usuario_crea: UUID


class ProductoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    id_usuario_edita: UUID | None = None


class ProductoResponse(ProductoBase):
    id_producto: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None
    id_usuario_crea: UUID
    id_usuario_edita: UUID | None = None

    class Config:
        from_attributes = True
