"""Repository helpers for Module 1 crime database operations."""

from __future__ import annotations

from datetime import date

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from .models import CrimeRecord
from .schemas import CrimeRecordCreate


def create_crime_record(session: Session, payload: CrimeRecordCreate) -> CrimeRecord:
    """Insert one crime record."""

    record = CrimeRecord(**payload.model_dump())
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def get_crime_record_by_crime_id(session: Session, crime_id: str) -> CrimeRecord | None:
    """Find one record by its external crime ID."""

    return session.scalar(select(CrimeRecord).where(CrimeRecord.crime_id == crime_id))


def search_crime_records(
    session: Session,
    *,
    district: str | None = None,
    police_station: str | None = None,
    crime_type: str | None = None,
    status: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    limit: int = 100,
) -> list[CrimeRecord]:
    """Search records using filters commonly needed by chatbot and dashboards."""

    query: Select[tuple[CrimeRecord]] = select(CrimeRecord)

    if district:
        query = query.where(CrimeRecord.district == district)
    if police_station:
        query = query.where(CrimeRecord.police_station == police_station)
    if crime_type:
        query = query.where(CrimeRecord.crime_type == crime_type)
    if status:
        query = query.where(CrimeRecord.status == status)
    if from_date:
        query = query.where(CrimeRecord.crime_date >= from_date)
    if to_date:
        query = query.where(CrimeRecord.crime_date <= to_date)

    query = query.order_by(CrimeRecord.crime_date.desc(), CrimeRecord.id.desc()).limit(limit)
    return list(session.scalars(query))
