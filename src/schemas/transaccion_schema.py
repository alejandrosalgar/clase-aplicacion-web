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
    id_usuario_creacion: UUID


class TransaccionUpdate(BaseModel):
    descripcion: str | None = None
    id_usuario_edita: UUID | None = None


class TransaccionResponse(TransaccionBase):
    id_transacciones: UUID
    id_usuario_creacion: UUID
    fecha: datetime | None = None
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
