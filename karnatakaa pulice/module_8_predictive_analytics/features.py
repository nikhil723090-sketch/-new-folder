"""Feature engineering for crime prediction."""

from __future__ import annotations

import pandas as pd


def build_monthly_features(records: pd.DataFrame) -> pd.DataFrame:
    """Aggregate crime data into monthly district/type features."""

    df = records.copy()
    df["crime_date"] = pd.to_datetime(df["crime_date"], errors="coerce")
    df["month"] = df["crime_date"].dt.to_period("M").dt.to_timestamp()
    grouped = (
        df.groupby(["district", "crime_type", "month"])
        .size()
        .reset_index(name="crime_count")
        .sort_values(["district", "crime_type", "month"])
    )
    grouped["previous_crime_count"] = grouped.groupby(["district", "crime_type"])["crime_count"].shift(1).fillna(0)
    grouped["month_number"] = grouped["month"].dt.month
    grouped["year"] = grouped["month"].dt.year
    return grouped


def add_external_features(
    features: pd.DataFrame,
    weather: pd.DataFrame | None = None,
    festivals: pd.DataFrame | None = None,
    population: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Attach optional weather, festival, and population features."""

    enriched = features.copy()
    for optional in [weather, festivals, population]:
        if optional is not None:
            enriched = enriched.merge(optional, how="left")
    return enriched.fillna(0)
