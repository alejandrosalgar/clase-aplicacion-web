from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class CuentaBase(BaseModel):
    numero_cuenta: str = Field(..., min_length=1, max_length=50, description="Número de cuenta único")
    id_usuario: UUID = Field(..., description="ID del titular")
    id_sucursal: UUID = Field(..., description="ID de la sucursal")
    id_tipo_cuenta: UUID = Field(..., description="ID del tipo de cuenta")


class CuentaCreate(CuentaBase):
    saldo: Decimal | None = Field(default=0, ge=0, description="Saldo inicial (no negativo)")
    id_usuario_creacion: UUID


class CuentaUpdate(BaseModel):
    numero_cuenta: str | None = Field(None, min_length=1, max_length=50)
    id_sucursal: UUID | None = None
    id_tipo_cuenta: UUID | None = None
    saldo: Decimal | None = Field(None, ge=0)
    id_usuario_edita: UUID | None = None


class CuentaResponse(CuentaBase):
    id_cuenta: UUID
    saldo: Decimal
    id_usuario_creacion: UUID
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
