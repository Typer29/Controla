"""User model."""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    """Represents a user on a device."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    sid: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
