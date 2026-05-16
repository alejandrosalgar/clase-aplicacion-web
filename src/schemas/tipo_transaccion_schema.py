from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TipoTransaccionBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Código único del tipo")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del tipo de transacción")


class TipoTransaccionCreate(TipoTransaccionBase):
    id_usuario_creacion: UUID


class TipoTransaccionUpdate(BaseModel):
    codigo: str | None = Field(None, min_length=1, max_length=20)
    nombre: str | None = Field(None, min_length=1, max_length=100)
    id_usuario_edita: UUID | None = None


class TipoTransaccionResponse(TipoTransaccionBase):
    id_tipo_transaccion: UUID
    id_usuario_creacion: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
