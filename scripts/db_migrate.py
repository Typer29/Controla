"""Run Alembic database migrations."""
from __future__ import annotations

import argparse
from pathlib import Path

from alembic import command
from alembic.config import Config


def main() -> None:
    parser = argparse.ArgumentParser(description="Run database migrations")
    parser.add_argument(
        "action",
        choices=["upgrade", "downgrade"],
        help="Alembic action",
    )
    parser.add_argument(
        "revision", nargs="?", default="head", help="Target revision"
    )
    args = parser.parse_args()

    cfg_path = (
        Path(__file__).resolve().parent.parent
        / "db"
        / "migrations"
        / "alembic.ini"
    )
    alembic_cfg = Config(str(cfg_path))

    if args.action == "upgrade":
        command.upgrade(alembic_cfg, args.revision)
    else:
        command.downgrade(alembic_cfg, args.revision)


if __name__ == "__main__":
    main()
