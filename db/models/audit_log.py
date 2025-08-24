"""Audit log model."""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AuditLog(Base):
    """Records administrative actions."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    target: Mapped[str | None] = mapped_column(String(255))
    ts: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    detail_json: Mapped[str | None] = mapped_column(Text)
