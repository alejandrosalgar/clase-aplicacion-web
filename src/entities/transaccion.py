import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Transaccion(Base):
    __tablename__ = "transaccion"

    id_transacciones = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_cuenta = Column(
        UUID(as_uuid=True), ForeignKey("cuenta.id_cuenta"), nullable=False
    )
    id_tipo_transaccion = Column(
        UUID(as_uuid=True),
        ForeignKey("tipo_transaccion.id_tipo_transaccion"),
        nullable=False,
    )
    id_cuenta_destino = Column(
        UUID(as_uuid=True), ForeignKey("cuenta.id_cuenta"), nullable=True
    )

    monto = Column(Numeric(15, 2), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    cuenta = relationship(
        "Cuenta", back_populates="transacciones", foreign_keys=[id_cuenta]
    )
    tipo_transaccion = relationship("TipoTransaccion", back_populates="transacciones")
    cuenta_destino = relationship("Cuenta", foreign_keys=[id_cuenta_destino])
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
