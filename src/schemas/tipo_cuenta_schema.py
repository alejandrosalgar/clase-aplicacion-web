from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TipoCuentaBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Código único del tipo")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del tipo de cuenta")


class TipoCuentaCreate(TipoCuentaBase):
    id_usuario_creacion: UUID


class TipoCuentaUpdate(BaseModel):
    codigo: str | None = Field(None, min_length=1, max_length=20)
    nombre: str | None = Field(None, min_length=1, max_length=100)
    id_usuario_edita: UUID | None = None


class TipoCuentaResponse(TipoCuentaBase):
    id_tipo_cuenta: UUID
    id_usuario_creacion: UUID
    id_usuario_edita: UUID | None = None
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
