"""Initial database schema."""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("hostname", sa.String(255), nullable=False, unique=True),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(255), nullable=False, unique=True),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_table(
        "apps",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("exe_path", sa.String(1024), nullable=False),
        sa.Column("file_hash_sha256", sa.String(64), nullable=False),
    )
    op.create_table(
        "app_sessions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("app_id", sa.Integer, sa.ForeignKey("apps.id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("device_id", sa.Integer, sa.ForeignKey("devices.id"), nullable=False),
        sa.Column("pid", sa.Integer, nullable=False),
        sa.Column("started_at", sa.DateTime, nullable=False),
        sa.Column("ended_at", sa.DateTime, nullable=False),
        sa.Column("active_seconds", sa.Integer, nullable=False),
        sa.Column("window_title_sample", sa.String(1024)),
    )
    op.create_table(
        "web_domains",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("domain", sa.String(255), nullable=False, unique=True),
    )
    op.create_table(
        "web_sessions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "domain_id",
            sa.Integer,
            sa.ForeignKey("web_domains.id"),
            nullable=False,
        ),
        sa.Column("browser", sa.String(50), nullable=False),
        sa.Column("url", sa.String(2048), nullable=False),
        sa.Column("title", sa.String(1024), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("device_id", sa.Integer, sa.ForeignKey("devices.id"), nullable=False),
        sa.Column("started_at", sa.DateTime, nullable=False),
        sa.Column("ended_at", sa.DateTime, nullable=False),
        sa.Column("active_seconds", sa.Integer, nullable=False),
    )
    op.create_table(
        "overrides",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("target_type", sa.String(50), nullable=False),
        sa.Column("target_id", sa.Integer, nullable=False),
        sa.Column("label", sa.String(255), nullable=False),
        sa.Column("category", sa.String(255)),
    )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("device_id", sa.Integer, sa.ForeignKey("devices.id")),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("details", sa.Text),
    )

def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("overrides")
    op.drop_table("web_sessions")
    op.drop_table("web_domains")
    op.drop_table("app_sessions")
    op.drop_table("apps")
    op.drop_table("users")
    op.drop_table("devices")
