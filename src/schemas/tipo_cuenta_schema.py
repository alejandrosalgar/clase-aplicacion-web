from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TipoCuentaBase(BaseModel):
    codigo: str
    nombre: str


class TipoCuentaCreate(TipoCuentaBase):
    pass


class TipoCuentaUpdate(BaseModel):
    codigo: str | None = None
    nombre: str | None = None


class TipoCuentaResponse(TipoCuentaBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
