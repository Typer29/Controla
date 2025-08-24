"""Device model."""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Device(Base):
    """Represents a physical or virtual machine."""

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    os_version: Mapped[str] = mapped_column(String(255), nullable=False)
    installed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    owner: Mapped[str | None] = mapped_column(String(255))
