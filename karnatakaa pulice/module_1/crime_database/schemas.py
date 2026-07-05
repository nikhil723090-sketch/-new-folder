"""Validation schemas for crime records."""

from __future__ import annotations

from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, Field


class CrimeRecordCreate(BaseModel):
    """Input schema for creating a crime record."""

    crime_id: str = Field(min_length=1, max_length=40)
    police_station: str = Field(min_length=1, max_length=120)
    district: str = Field(min_length=1, max_length=120)
    crime_type: str = Field(min_length=1, max_length=120)
    crime_date: date
    crime_time: time | None = None
    victim: str | None = Field(default=None, max_length=160)
    suspect: str | None = Field(default=None, max_length=160)
    vehicle: str | None = Field(default=None, max_length=120)
    weapon: str | None = Field(default=None, max_length=120)
    latitude: Decimal = Field(ge=Decimal("11.0"), le=Decimal("19.5"))
    longitude: Decimal = Field(ge=Decimal("74.0"), le=Decimal("79.5"))
    status: str = Field(min_length=1, max_length=40)
    notes: str | None = None


class CrimeRecordRead(CrimeRecordCreate):
    """Output schema for API responses."""

    id: int

    class Config:
        from_attributes = True
