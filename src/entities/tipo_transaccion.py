import uuid

from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class TipoTransaccion(Base):
    __tablename__ = "tipo_transaccion"

    id_tipo_transaccion = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(80), nullable=False)

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    transacciones = relationship("Transaccion", back_populates="tipo_transaccion")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
