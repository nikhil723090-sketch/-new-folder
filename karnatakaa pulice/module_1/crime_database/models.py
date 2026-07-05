"""SQLAlchemy models for structured crime records."""

from __future__ import annotations

from datetime import date, datetime, time
from decimal import Decimal

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, Time, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for ORM models."""


class CrimeRecord(Base):
    """Core crime record used by chatbot queries, analytics, and maps."""

    __tablename__ = "crime_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crime_id: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    police_station: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    district: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    crime_type: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    crime_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    crime_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    victim: Mapped[str | None] = mapped_column(String(160), nullable=True)
    suspect: Mapped[str | None] = mapped_column(String(160), index=True, nullable=True)
    vehicle: Mapped[str | None] = mapped_column(String(120), nullable=True)
    weapon: Mapped[str | None] = mapped_column(String(120), nullable=True)
    latitude: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    status: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
