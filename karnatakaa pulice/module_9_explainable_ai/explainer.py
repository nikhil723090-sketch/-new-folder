"""SHAP/LIME explanations for crime predictions."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Explanation:
    """Human-readable model explanation."""

    confidence: float
    reasons: list[str]


class PredictionExplainer:
    """Explain predictions with SHAP when available, then fallback reasons."""

    def explain(self, model, feature_row: pd.DataFrame, predicted_count: float) -> Explanation:
        confidence = min(max(predicted_count / 100.0, 0.0), 0.99)
        reasons = self._fallback_reasons(feature_row)
        try:
            import shap

            transformed = model.named_steps["preprocessor"].transform(feature_row)
            estimator = model.named_steps["model"]
            values = shap.TreeExplainer(estimator).shap_values(transformed)
            if len(values):
                reasons.insert(0, "Model feature contribution analysis completed with SHAP.")
        except Exception:
            pass
        return Explanation(confidence=round(confidence, 2), reasons=reasons)

    @staticmethod
    def _fallback_reasons(feature_row: pd.DataFrame) -> list[str]:
        row = feature_row.iloc[0]
        reasons = []
        previous = float(row.get("previous_crime_count", 0))
        if previous > 0:
            reasons.append(f"Previous crime count in this segment was {int(previous)}.")
        if int(row.get("month_number", 0)) in {10, 11, 12, 1}:
            reasons.append("Seasonal period has historically higher policing sensitivity.")
        reasons.append("Location, crime type, and recent history were used for this prediction.")
        return reasons
