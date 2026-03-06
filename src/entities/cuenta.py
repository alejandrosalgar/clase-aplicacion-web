import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Cuenta(Base):
    __tablename__ = "tbl_cuentas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    numero_cuenta = Column(String(30), unique=True, nullable=False, index=True)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("tbl_usuarios.id"), nullable=False)
    id_sucursal = Column(UUID(as_uuid=True), ForeignKey("tbl_sucursales.id"), nullable=False)
    id_tipo_cuenta = Column(UUID(as_uuid=True), ForeignKey("tbl_tipos_cuenta.id"), nullable=False)
    saldo = Column(Numeric(15, 2), default=0, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    usuario = relationship("Usuario", back_populates="cuentas")
    sucursal = relationship("Sucursal", back_populates="cuentas")
    tipo_cuenta = relationship("TipoCuenta", back_populates="cuentas")
    transacciones = relationship("Transaccion", back_populates="cuenta", foreign_keys="Transaccion.id_cuenta")
