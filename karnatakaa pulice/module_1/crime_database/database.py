"""SQLAlchemy engine and session factory for the crime database."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_database_settings


settings = get_database_settings()
engine = create_engine(settings.url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session for API handlers or scripts."""

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
