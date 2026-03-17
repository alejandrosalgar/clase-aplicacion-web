import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base
from src.entities.transaccion import Transaccion


class Cuenta(Base):
    __tablename__ = "cuenta"

    id_cuenta = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_sucursal = Column(
        UUID(as_uuid=True), ForeignKey("sucursal.id_sucursal"), nullable=False
    )
    id_tipo_cuenta = Column(
        UUID(as_uuid=True), ForeignKey("tipo_cuenta.id_tipo_cuenta"), nullable=False
    )

    numero_cuenta = Column(String(30), unique=True, nullable=False, index=True)
    saldo = Column(Numeric(15, 2), default=0, nullable=False)

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    sucursal = relationship("Sucursal", back_populates="cuentas")
    tipo_cuenta = relationship("TipoCuenta", back_populates="cuentas")
    transacciones = relationship(
        "Transaccion", back_populates="cuenta", foreign_keys=[Transaccion.id_cuenta]
    )
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    