"""Crime pattern detection using pandas group-by analytics."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class PatternSummary:
    """High-level pattern detection result."""

    peak_crime_hours: pd.DataFrame
    crime_by_season: pd.DataFrame
    crime_by_district: pd.DataFrame
    repeat_offenders: pd.DataFrame
    repeat_locations: pd.DataFrame


class CrimePatternDetector:
    """Find operational crime patterns from structured records."""

    def __init__(self, records: pd.DataFrame) -> None:
        self.records = records

    def peak_crime_hours(self, limit: int = 10) -> pd.DataFrame:
        """Return the hours with the most crimes."""

        return (
            self.records.dropna(subset=["crime_hour"])
            .groupby("crime_hour")
            .size()
            .reset_index(name="case_count")
            .sort_values("case_count", ascending=False)
            .head(limit)
        )

    def crime_by_season(self) -> pd.DataFrame:
        """Return crime volume grouped by season."""

        return (
            self.records.groupby(["season", "crime_type"])
            .size()
            .reset_index(name="case_count")
            .sort_values("case_count", ascending=False)
        )

    def crime_by_district(self) -> pd.DataFrame:
        """Return crime volume grouped by district and type."""

        return (
            self.records.groupby(["district", "crime_type"])
            .size()
            .reset_index(name="case_count")
            .sort_values("case_count", ascending=False)
        )

    def repeat_offenders(self, min_cases: int = 2) -> pd.DataFrame:
        """Find suspects appearing in multiple cases."""

        suspects = self.records.dropna(subset=["suspect"]).copy()
        suspects = suspects[suspects["suspect"].str.lower() != "unknown"]
        grouped = (
            suspects.groupby("suspect")
            .agg(case_count=("crime_id", "count"), districts=("district", lambda values: sorted(set(values))))
            .reset_index()
            .sort_values("case_count", ascending=False)
        )
        return grouped[grouped["case_count"] >= min_cases]

    def repeat_locations(self, min_cases: int = 2, precision: int = 3) -> pd.DataFrame:
        """Find repeated crime locations by rounded latitude/longitude."""

        locations = self.records.dropna(subset=["latitude", "longitude"]).copy()
        locations["lat_bucket"] = locations["latitude"].astype(float).round(precision)
        locations["lon_bucket"] = locations["longitude"].astype(float).round(precision)
        grouped = (
            locations.groupby(["lat_bucket", "lon_bucket", "district"])
            .agg(case_count=("crime_id", "count"), crime_types=("crime_type", lambda values: sorted(set(values))))
            .reset_index()
            .sort_values("case_count", ascending=False)
        )
        return grouped[grouped["case_count"] >= min_cases]

    def summary(self) -> PatternSummary:
        """Run all pattern detectors."""

        return PatternSummary(
            peak_crime_hours=self.peak_crime_hours(),
            crime_by_season=self.crime_by_season(),
            crime_by_district=self.crime_by_district(),
            repeat_offenders=self.repeat_offenders(),
            repeat_locations=self.repeat_locations(),
        )
