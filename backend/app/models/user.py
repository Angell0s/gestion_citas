# backend\app\models\user.py
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, time
from sqlalchemy import DateTime, ForeignKey, Index, String, text
from sqlalchemy.sql import func
from typing import List

from .mixin import TimestampMixin


from . import Base

class User(Base, TimestampMixin):
    __tablename__ = "users"

    __table_args__ = (
        Index("ix_users_username_lower", func.lower(text("username"))),
        Index("ix_users_email", func.lower(text("email"))),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_system_admin: Mapped[bool] = mapped_column(default=False)

    # Nuevo campo
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    businesses: Mapped[list["Businesses"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    memberships: Mapped[List["BusinessMember"]] = relationship(
        "BusinessMember", back_populates="user"
    )
    appointments: Mapped[List["Appointment"]] = relationship(
        "Appointment", back_populates="employee"
    )