"""Resolve short follow-up questions using previous conversation context."""

from __future__ import annotations

import re

from module_2_ai_chatbot.nl_to_sql import CRIME_TYPES, DISTRICT_ALIASES

from .memory import ChatTurn


FOLLOW_UP_PREFIXES = (
    "only in",
    "what about",
    "show only",
    "filter by",
    "in ",
)


def resolve_follow_up(question: str, history: list[ChatTurn]) -> str:
    """Expand a follow-up question into a standalone question."""

    normalized = re.sub(r"\s+", " ", question.lower()).strip()
    if not history or _has_crime_type(normalized):
        return question

    district = _find_district(normalized)
    if not district or not _looks_like_follow_up(normalized):
        return question

    previous_crime_type = _last_crime_type(history)
    if not previous_crime_type:
        return question

    return f"Show {previous_crime_type.lower()} cases in {district}."


def _looks_like_follow_up(normalized: str) -> bool:
    return normalized.startswith(FOLLOW_UP_PREFIXES) or len(normalized.split()) <= 5


def _find_district(normalized: str) -> str | None:
    for alias, district in DISTRICT_ALIASES.items():
        if alias in normalized:
            return district
    return None


def _has_crime_type(normalized: str) -> bool:
    return any(phrase in normalized for phrase in CRIME_TYPES)


def _last_crime_type(history: list[ChatTurn]) -> str | None:
    for turn in reversed(history):
        text = f"{turn.user_message} {turn.sql or ''}".lower()
        for phrase, crime_type in sorted(CRIME_TYPES.items(), key=lambda item: len(item[0]), reverse=True):
            if phrase in text or crime_type.lower() in text:
                return crime_type
    return None
