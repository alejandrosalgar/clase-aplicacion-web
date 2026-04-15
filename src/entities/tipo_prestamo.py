from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from src.database.config import Base


class TipoPrestamo(Base):
    __tablename__ = "tipo_prestamo"

    id_tipo_prestamo = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    nombre = Column(
        String(100), nullable=False)
    
    descripcion = Column(String(255))

    estado = Column(String(50), nullable=False)

    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    
    id_usuario_edita = Column(UUID(as_uuid=True), nullable=True)

    # auditoría
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())