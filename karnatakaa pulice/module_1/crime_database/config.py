"""Database configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseSettings:
    """Connection settings loaded from environment variables."""

    url: str


def get_database_settings() -> DatabaseSettings:
    """Return database settings.

    Examples:
        PostgreSQL:
            DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/scrb

        MySQL:
            DATABASE_URL=mysql+pymysql://user:password@localhost:3306/scrb
    """

    return DatabaseSettings(
        url=os.getenv("DATABASE_URL", "postgresql+psycopg://scrb:scrb@localhost:5432/scrb")
    )
