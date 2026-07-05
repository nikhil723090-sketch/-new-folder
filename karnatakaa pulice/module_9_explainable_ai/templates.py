"""Text templates for explainable AI outputs."""

from __future__ import annotations

from .explainer import Explanation


def format_explanation(explanation: Explanation) -> str:
    lines = [f"Prediction confidence: {int(explanation.confidence * 100)}%", "Reasons:"]
    lines.extend(f"- {reason}" for reason in explanation.reasons)
    return "\n".join(lines)
