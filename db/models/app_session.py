"""App session model."""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AppSession(Base):
    """Period of time an application was in foreground."""

    __tablename__ = "app_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    app_id: Mapped[int] = mapped_column(ForeignKey("apps.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    pid: Mapped[int] = mapped_column(Integer, nullable=False)
    started_at: Mapped[datetime] = mapped_column(nullable=False)
    ended_at: Mapped[datetime] = mapped_column(nullable=False)
    active_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    window_title_sample: Mapped[str | None] = mapped_column(String(1024))
