from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TipoCuentaBase(BaseModel):
    codigo: str
    nombre: str


class TipoCuentaCreate(TipoCuentaBase):
    id_usuario_creacion: UUID


class TipoCuentaUpdate(BaseModel):
    codigo: str | None = None
    nombre: str | None = None
    id_usuario_edita: UUID | None = None


class TipoCuentaResponse(TipoCuentaBase):
    id_tipo_cuenta: UUID
    id_usuario_creacion: UUID
    id_usuario_edita: UUID | None = None
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
