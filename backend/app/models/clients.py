import uuid
from typing import List
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, String

from .mixin import TimestampMixin
from . import Base

# CORRECCIÓN: Clase en PascalCase
class Client(Base, TimestampMixin):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("businesses.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    # Cambié el unique=True de email. Un cliente puede ir a dos negocios con el mismo email.
    email: Mapped[str] = mapped_column(String(255), nullable=True, index=True) 
    notes: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # CORRECCIÓN: Nombre de la clase en string
    business: Mapped["Businesses"] = relationship("Businesses", back_populates="clients")
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="client", cascade="all, delete-orphan")

    # NUEVO: Índice para que un negocio no duplique al mismo teléfono
    __table_args__ = (
        Index("ix_client_business_phone", "business_id", "phone", unique=True),
    )

class ClientReputation(Base, TimestampMixin):
    __tablename__ = "client_reputation"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    reporting_business_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("businesses.id"), nullable=False, index=True
    )
    phone: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=True)
    
    # flag_type: 'good_client', 'no_show', 'fraud', etc.
    flag_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_locally_blocked: Mapped[bool] = mapped_column(default=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)

    __table_args__ = (
        Index("ix_unique_reputation_per_business", "reporting_business_id", "phone", unique=True),
    )
    
    # CORRECCIÓN: Agregado back_populates
    business: Mapped["Businesses"] = relationship("Businesses", back_populates="clients_reputation")