from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from enum import Enum


class EstadoTipoPrestamo(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


class TipoPrestamoBase(BaseModel):
    nombre: str = Field(
        ..., min_length=1, max_length=100, description="nombre del tipo de prestamo"
    )
    descripcion: str | None = Field(
        None, max_length=255, description="descripcion del tipo de prestamo"
    )


class TipoPrestamoCreate(TipoPrestamoBase):
    id_usuario_creacion: UUID
    estado: EstadoTipoPrestamo = EstadoTipoPrestamo.ACTIVO


class TipoPrestamoUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    descripcion: str | None = Field(None, max_length=255)
    estado: EstadoTipoPrestamo | None = None
    id_usuario_edita: UUID | None = None


class TipoPrestamoResponse(TipoPrestamoBase):
    id_tipo_prestamo: UUID
    estado: EstadoTipoPrestamo

    id_usuario_creacion: UUID
    id_usuario_edita: UUID | None = None

    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True