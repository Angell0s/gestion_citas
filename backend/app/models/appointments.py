# backend\app\models\appointments.py

import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, time
from sqlalchemy import DateTime, ForeignKey, Index, String, text, Numeric
from sqlalchemy.sql import func
from typing import List
from decimal import Decimal

from .mixin import TimestampMixin
from . import Base

class Service(Base, TimestampMixin):
    __tablename__ = "services"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("businesses.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    business: Mapped["Businesses"] = relationship("Businesses", back_populates="services")
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="service")

class Appointment(Base, TimestampMixin):
    __tablename__ = "appointments"

    __table_args__ = (
        # Índice de tiempo para consultas de disponibilidad y reportes/dashboards
        Index("ix_appointments_business_time", "business_id", "start_at"),
        
        # Índice de estado de reportes, útil para dashboards de rendimiento y para filtrar rápidamente citas activas vs canceladas
        Index("ix_appointments_business_status", "business_id", "status"),
        
        # Índice de empledado para reportes de productividad, entre otros
        Index("ix_appointments_business_employee_time", "business_id", "employee_id", "start_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("businesses.id"), nullable=False, index=True
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("clients.id"), nullable=False, index=True
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=True, index=True
    )
    service_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("services.id"), nullable=False, index=True
    )
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="scheduled")
    notes: Mapped[str] = mapped_column(String(500), nullable=True)

    business: Mapped["Businesses"] = relationship("Businesses", back_populates="appointments")
    client: Mapped["Client"] = relationship("Client", back_populates="appointments")
    employee: Mapped["User"] = relationship("User", back_populates="appointments")
    service: Mapped["Service"] = relationship("Service", back_populates="appointments")