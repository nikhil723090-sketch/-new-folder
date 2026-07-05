"""Safety checks for LLM-generated SQL."""

from __future__ import annotations

import re


BLOCKED_KEYWORDS = {
    "alter",
    "create",
    "delete",
    "drop",
    "grant",
    "insert",
    "merge",
    "revoke",
    "truncate",
    "update",
}


def ensure_safe_select(sql: str) -> str:
    """Validate and normalize SQL before execution."""

    cleaned = _strip_markdown(sql).strip().rstrip(";")
    lowered = cleaned.lower()
    tokens = set(re.findall(r"[a-z_]+", lowered))

    if not lowered.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    if BLOCKED_KEYWORDS.intersection(tokens):
        raise ValueError("Unsafe SQL keyword detected.")
    if "crime_records" not in lowered:
        raise ValueError("Queries must use the crime_records table.")
    if ";" in cleaned:
        raise ValueError("Multiple SQL statements are not allowed.")

    if " limit " not in lowered and "count(" not in lowered:
        cleaned = f"{cleaned} LIMIT 100"

    return cleaned


def _strip_markdown(sql: str) -> str:
    if sql.startswith("```"):
        return sql.replace("```sql", "").replace("```", "").strip()
    return sql
