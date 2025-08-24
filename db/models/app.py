"""Application model."""
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class App(Base):
    """Tracked application executable."""

    __tablename__ = "apps"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    exe_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    file_hash_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
