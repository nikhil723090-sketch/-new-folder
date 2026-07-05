"""ML models for crime risk and next-month prediction."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class PredictionResult:
    """Prediction output."""

    district: str
    crime_type: str
    predicted_count: float
    hotspot_probability: float
    risk_level: str


class CrimeRiskPredictor:
    """Train a Random Forest model for monthly crime count prediction."""

    def __init__(self) -> None:
        from sklearn.compose import ColumnTransformer
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder

        categorical = ["district", "crime_type"]
        numeric = ["previous_crime_count", "month_number", "year"]
        preprocessor = ColumnTransformer(
            transformers=[
                ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
                ("numeric", "passthrough", numeric),
            ]
        )
        self.model = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", RandomForestRegressor(n_estimators=100, random_state=42)),
            ]
        )

    def train(self, features: pd.DataFrame) -> None:
        x = features[["district", "crime_type", "previous_crime_count", "month_number", "year"]]
        y = features["crime_count"]
        self.model.fit(x, y)

    def predict_next_month(self, feature_rows: pd.DataFrame) -> list[PredictionResult]:
        x = feature_rows[["district", "crime_type", "previous_crime_count", "month_number", "year"]]
        predictions = self.model.predict(x)
        results: list[PredictionResult] = []
        for (_, row), predicted in zip(feature_rows.iterrows(), predictions, strict=False):
            probability = min(float(predicted) / max(float(row.get("previous_crime_count", 1)), 1.0), 1.0)
            results.append(
                PredictionResult(
                    district=str(row["district"]),
                    crime_type=str(row["crime_type"]),
                    predicted_count=round(float(predicted), 2),
                    hotspot_probability=round(probability, 3),
                    risk_level=_risk_level(probability),
                )
            )
        return results


def _risk_level(probability: float) -> str:
    if probability >= 0.75:
        return "High"
    if probability >= 0.4:
        return "Medium"
    return "Low"
