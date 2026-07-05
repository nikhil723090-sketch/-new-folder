"""Turn SQL rows into investigator-friendly answers."""

from __future__ import annotations

from typing import Any


def format_answer(question: str, sql: str, rows: list[dict[str, Any]]) -> str:
    """Create a concise human-readable response."""

    if not rows:
        return "No matching crime records were found for this question."

    first = rows[0]
    if "total_cases" in first:
        total = first["total_cases"]
        return f"There were {total} matching crime cases for your question."

    lines = [f"Found {len(rows)} matching crime records."]
    for row in rows[:5]:
        lines.append(
            "- {crime_id}: {crime_type} in {district} at {police_station} "
            "on {crime_date}; status: {status}".format(**row)
        )

    if len(rows) > 5:
        lines.append(f"...and {len(rows) - 5} more records.")

    return "\n".join(lines)
