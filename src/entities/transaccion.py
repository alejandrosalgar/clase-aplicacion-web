import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Transaccion(Base):
    __tablename__ = "tbl_transacciones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_cuenta = Column(UUID(as_uuid=True), ForeignKey("tbl_cuentas.id"), nullable=False)
    id_tipo_transaccion = Column(
        UUID(as_uuid=True), ForeignKey("tbl_tipos_transaccion.id"), nullable=False
    )
    monto = Column(Numeric(15, 2), nullable=False)
    id_cuenta_destino = Column(UUID(as_uuid=True), ForeignKey("tbl_cuentas.id"), nullable=True)
    descripcion = Column(Text, nullable=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    cuenta = relationship("Cuenta", back_populates="transacciones", foreign_keys=[id_cuenta])
    tipo_transaccion = relationship("TipoTransaccion", back_populates="transacciones")
    cuenta_destino = relationship("Cuenta", foreign_keys=[id_cuenta_destino])
