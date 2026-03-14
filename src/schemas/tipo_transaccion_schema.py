from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TipoTransaccionBase(BaseModel):
    codigo: str
    nombre: str


class TipoTransaccionCreate(TipoTransaccionBase):
    id_usuario_creacion: UUID


class TipoTransaccionUpdate(BaseModel):
    codigo: str | None = None
    nombre: str | None = None
    id_usuario_edita: UUID | None = None


class TipoTransaccionResponse(TipoTransaccionBase):
    id_tipo_transaccion: UUID
    id_usuario_creacion: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
