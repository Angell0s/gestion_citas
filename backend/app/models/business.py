# backend\app\models\business.py

import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, time
from sqlalchemy import DateTime, ForeignKey, Index, String, text
from sqlalchemy.sql import func
from typing import List

from .mixin import TimestampMixin
from . import Base

class Businesses(Base, TimestampMixin):
    __tablename__ = "businesses"

    __table_args__ = (
        Index("ix_businesses_owner_name", "owner_id", "name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    logo: Mapped[str] = mapped_column(String(255), nullable=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    timezone: Mapped[str] = mapped_column(String(50), server_default="UTC", default="America/Mexico_City", nullable=False)
    
    # Relaciones
    owner: Mapped["User"] = relationship("User", back_populates="businesses")
    business_hours: Mapped[List["BusinessHours"]] = relationship(back_populates="business", cascade="all, delete-orphan")
    
    # NUEVA: Relación con los miembros (empleados/staff) del negocio
    members: Mapped[List["BusinessMember"]] = relationship(back_populates="business", cascade="all, delete-orphan")

    clients: Mapped[List["Client"]] = relationship(
        "Client", back_populates="business", cascade="all, delete-orphan"
    )

    clients_reputation: Mapped[List["ClientReputation"]] = relationship(
        "ClientReputation", back_populates="business", cascade="all, delete-orphan"
    )

    services: Mapped[List["Service"]] = relationship(
        "Service", back_populates="business", cascade="all, delete-orphan"
    )

    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment", back_populates="business", cascade="all, delete-orphan"
    )

class BusinessHours(Base, TimestampMixin):
    __tablename__ = "business_hours"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("businesses.id"), nullable=False, index=True
    )
    laboral_days: Mapped[int] = mapped_column(nullable=False)
    open_time: Mapped[time] = mapped_column(nullable=False)
    close_time: Mapped[time] = mapped_column(nullable=False)
    
    business: Mapped["Businesses"] = relationship("Businesses", back_populates="business_hours")

class Role(Base): # Renombrado a Role (Singular + CamelCase)
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    superuser: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relación con los miembros que tienen este rol
    members: Mapped[List["BusinessMember"]] = relationship(back_populates="role")

class BusinessMember(Base, TimestampMixin): # Renombrado a BusinessMember
    __tablename__ = "business_members"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    business_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("businesses.id"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.id"), nullable=False, index=True
    )

    # Relaciones para acceder a los objetos completos
    business: Mapped["Businesses"] = relationship("Businesses", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="memberships")
    role: Mapped["Role"] = relationship("Role", back_populates="members")