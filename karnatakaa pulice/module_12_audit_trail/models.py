"""SQLAlchemy model for legal/compliance audit logs."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AuditBase(DeclarativeBase):
    """Base class for audit models."""


class AuditLog(AuditBase):
    """Stores who did what, when, and what AI/database output was produced."""

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    role: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    action: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    question: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    generated_sql: Mapped[str | None] = mapped_column(Text, nullable=True)
    prediction: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
