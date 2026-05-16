from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from decimal import Decimal
from enum import Enum


class EstadoPrestamo(str, Enum):
    ACTIVO = "ACTIVO"
    PAGADO = "PAGADO"
    MORA = "MORA"
    CANCELADO = "CANCELADO"


class PrestamoBase(BaseModel):
    valor: Decimal = Field(..., gt=0, description="valor del prestamo")
    interes: Decimal = Field(..., ge=0, description="interes del prestamo")
    plazo: int = Field(..., gt=0, description="plazo de pago en meses")
    id_usuario: UUID


class PrestamoCreate(PrestamoBase):
    id_usuario_creacion: UUID
    estado: EstadoPrestamo = EstadoPrestamo.ACTIVO


class PrestamoUpdate(BaseModel):
    valor: Decimal | None = Field(None, gt=0)
    interes: Decimal | None = Field(None, ge=0)
    plazo: int | None = Field(None, gt=0)
    id_usuario: UUID | None = None
    estado: EstadoPrestamo | None = None
    id_usuario_edita: UUID | None = None


class PrestamoResponse(PrestamoBase):
    id_prestamo: UUID
    valor_pendiente: Decimal
    estado: EstadoPrestamo

    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None

    fecha_creacion: datetime | None = None
    fecha_edicion: datetime | None = None

    id_usuario_creacion: UUID
    id_usuario_edita: UUID | None = None

    class config:
        from_attributes = True
