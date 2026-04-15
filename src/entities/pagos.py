from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from src.database.config import Base


class Pago(Base):
    __tablename__ = "pago"

    id_pago = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    id_prestamo = Column(UUID(as_uuid=True), ForeignKey("prestamo.id_prestamo"))

    monto = Column(Numeric(10, 2), nullable=False)

    fecha = Column(DateTime, default=datetime.utcnow)

    estado = Column(String(50), nullable=False)

    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)

    id_usuario_edita = Column(UUID(as_uuid=True), nullable=True)

    # auditoría
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
