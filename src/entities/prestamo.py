import uuid

from sqlalchemy import Column, DateTime, Integer, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Prestamo(Base):
    __tablename__ = "prestamo"

    id_prestamo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    valor = Column(Numeric(15, 2), nullable=False)
    valor_pendiente = Column(Numeric(15, 2), nullable=False)
    interes = Column(Numeric(5, 2), nullable=False)
    plazo = Column(Integer, nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default="ACTIVO",  # ACTIVO, PAGADO, MORA, CANCELADO
    )
    fecha_inicio = Column(DateTime(timezone=True), server_default=func.now())
    fecha_fin = Column(DateTime(timezone=True))

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
    usuario = relationship("Usuario", foreign_keys=[id_usuario])

    # auditoria----------
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
