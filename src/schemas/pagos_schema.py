from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from decimal import Decimal
from enum import Enum


class EstadoPago(str, Enum):
    PENDIENTE = "PENDIENTE"
    PAGADO = "PAGADO"
    FALLIDO = "FALLIDO"


class PagoBase(BaseModel):
    monto: Decimal = Field(..., gt=0, description="monto del pago")
    id_prestamo: UUID = Field(..., description="id del prestamo asociado")


class PagoCreate(PagoBase):
    id_usuario_creacion: UUID
    estado: EstadoPago = EstadoPago.PENDIENTE


class PagoUpdate(BaseModel):
    monto: Decimal | None = Field(None, gt=0)
    estado: EstadoPago | None = None
    id_usuario_edita: UUID | None = None


class PagoResponse(PagoBase):
    id_pago: UUID
    estado: EstadoPago

    fecha: datetime | None = None

    id_usuario_creacion: UUID
    id_usuario_edita: UUID | None = None

    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    class Config:
        from_attributes = True
