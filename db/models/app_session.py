"""App session model."""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, Index
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AppSession(Base):
    """Period of time an application was in foreground."""

    __tablename__ = "app_sessions"
    __table_args__ = (
        Index("ix_app_sessions_user_started_at", "user_id", "started_at"),
        Index("ix_app_sessions_app_started_at", "app_id", "started_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    app_id: Mapped[int] = mapped_column(ForeignKey("apps.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    pid: Mapped[int] = mapped_column(Integer, nullable=False)
    started_at: Mapped[datetime] = mapped_column(nullable=False)
    ended_at: Mapped[datetime] = mapped_column(nullable=False)
    active_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    window_title_sample: Mapped[str | None] = mapped_column(String(1024))
