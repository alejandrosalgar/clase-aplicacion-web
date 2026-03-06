from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TipoTransaccionBase(BaseModel):
    codigo: str
    nombre: str


class TipoTransaccionCreate(TipoTransaccionBase):
    pass


class TipoTransaccionUpdate(BaseModel):
    codigo: str | None = None
    nombre: str | None = None


class TipoTransaccionResponse(TipoTransaccionBase):
    id: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
