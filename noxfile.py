"""Nox sessions for development."""

import nox


@nox.session
def tests(session: nox.Session) -> None:
    """Run lint and tests."""
    session.install("ruff", "pytest")
    session.run("ruff", "check", ".")
    session.run("pytest")
