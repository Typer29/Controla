"""Web session model."""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class WebSession(Base):
    """Period of time a browser tab was in foreground."""

    __tablename__ = "web_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    domain_id: Mapped[int] = mapped_column(ForeignKey("web_domains.id"), nullable=False)
    browser: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    title: Mapped[str] = mapped_column(String(1024), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(nullable=False)
    ended_at: Mapped[datetime] = mapped_column(nullable=False)
    active_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
