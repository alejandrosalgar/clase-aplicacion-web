from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class TransaccionBase(BaseModel):
    id_cuenta: UUID
    id_tipo_transaccion: UUID
    monto: Decimal
    id_cuenta_destino: UUID | None = None
    descripcion: str | None = None


class TransaccionCreate(TransaccionBase):
    pass


class TransaccionUpdate(BaseModel):
    descripcion: str | None = None


class TransaccionResponse(TransaccionBase):
    id: UUID
    fecha: datetime | None = None

    class Config:
        from_attributes = True
