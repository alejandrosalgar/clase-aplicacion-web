from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class CuentaBase(BaseModel):
    numero_cuenta: str
    id_usuario: UUID
    id_sucursal: UUID
    id_tipo_cuenta: UUID


class CuentaCreate(CuentaBase):
    saldo: Decimal | None = 0


class CuentaUpdate(BaseModel):
    numero_cuenta: str | None = None
    id_sucursal: UUID | None = None
    id_tipo_cuenta: UUID | None = None
    saldo: Decimal | None = None


class CuentaResponse(CuentaBase):
    id: UUID
    saldo: Decimal
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
