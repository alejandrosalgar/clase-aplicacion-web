from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class TransaccionBase(BaseModel):
    id_cuenta: UUID = Field(..., description="Cuenta origen")
    id_tipo_transaccion: UUID = Field(..., description="Tipo de transacción")
    monto: Decimal = Field(..., gt=0, description="Monto (debe ser mayor que 0)")
    id_cuenta_destino: UUID | None = Field(None, description="Cuenta destino (transferencias)")
    descripcion: str | None = Field(None, max_length=500)


class TransaccionCreate(TransaccionBase):
    id_usuario_creacion: UUID


class TransaccionUpdate(BaseModel):
    descripcion: str | None = Field(None, max_length=500)
    id_usuario_edita: UUID | None = None


class TransaccionResponse(TransaccionBase):
    id_transacciones: UUID
    id_usuario_creacion: UUID
    fecha: datetime | None = None
    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
