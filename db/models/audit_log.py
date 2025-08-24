"""Audit log model."""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AuditLog(Base):
    """Records administrative actions."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    details: Mapped[str | None] = mapped_column(Text)
