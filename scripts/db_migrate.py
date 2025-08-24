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
    parser.add_argument(
        "--config",
        type=Path,
        default=(
            Path(__file__).resolve().parents[1]
            / "db"
            / "migrations"
            / "alembic.ini"
        ),
        help="Path to alembic.ini",
    )
    args = parser.parse_args()

    alembic_cfg = Config(str(args.config))

    if args.action == "upgrade":
        command.upgrade(alembic_cfg, args.revision)
    else:
        command.downgrade(alembic_cfg, args.revision)


if __name__ == "__main__":
    main()
