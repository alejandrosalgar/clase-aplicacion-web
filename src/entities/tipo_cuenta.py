import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class TipoCuenta(Base):
    __tablename__ = "tbl_tipos_cuenta"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(80), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    cuentas = relationship("Cuenta", back_populates="tipo_cuenta")

