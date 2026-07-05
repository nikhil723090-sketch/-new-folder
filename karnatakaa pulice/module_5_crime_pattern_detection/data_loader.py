"""Load crime records into pandas."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


REQUIRED_COLUMNS = {
    "crime_id",
    "police_station",
    "district",
    "crime_type",
    "crime_date",
    "crime_time",
    "victim",
    "suspect",
    "vehicle",
    "weapon",
    "latitude",
    "longitude",
    "status",
}


def load_from_database(session: "Session") -> pd.DataFrame:
    """Load records from the Module 1 database."""

    query = """
        SELECT crime_id, police_station, district, crime_type, crime_date, crime_time,
               victim, suspect, vehicle, weapon, latitude, longitude, status
        FROM crime_records
    """
    return normalize_dataframe(pd.read_sql_query(query, session.bind))


def load_from_csv(path: str | Path) -> pd.DataFrame:
    """Load records from a CSV export."""

    return normalize_dataframe(pd.read_csv(path))


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize date/time columns and validate required fields."""

    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required crime columns: {sorted(missing)}")

    normalized = df.copy()
    normalized["crime_date"] = pd.to_datetime(normalized["crime_date"], errors="coerce")
    normalized["crime_time"] = normalized["crime_time"].astype(str)
    normalized["crime_hour"] = pd.to_datetime(
        normalized["crime_time"], errors="coerce", format="%H:%M:%S"
    ).dt.hour
    normalized["month"] = normalized["crime_date"].dt.month
    normalized["season"] = normalized["month"].map(_season_for_month)
    return normalized


def _season_for_month(month: int | float) -> str:
    if pd.isna(month):
        return "Unknown"
    month = int(month)
    if month in {3, 4, 5}:
        return "Summer"
    if month in {6, 7, 8, 9}:
        return "Monsoon"
    if month in {10, 11}:
        return "Post-monsoon"
    return "Winter"
