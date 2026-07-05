"""Deterministic natural-language to SQL planner for common investigator queries."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from .llm_providers import SqlPlan


DISTRICT_ALIASES = {
    "bangalore": "Bengaluru Urban",
    "bengaluru": "Bengaluru Urban",
    "bengaluru urban": "Bengaluru Urban",
    "mysore": "Mysuru",
    "mysuru": "Mysuru",
    "hubli": "Dharwad",
    "hubballi": "Dharwad",
    "dharwad": "Dharwad",
}

CRIME_TYPES = {
    "burglary": "Burglary",
    "theft": "Theft",
    "vehicle theft": "Vehicle Theft",
    "robbery": "Robbery",
    "assault": "Assault",
    "fraud": "Fraud",
    "cyber crime": "Cyber Crime",
}

MONTHS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12",
}


@dataclass
class RuleBasedSqlPlanner:
    """Plan SQL for frequent crime database questions without an external LLM."""

    today: date = date.today()

    def plan(self, question: str) -> SqlPlan | None:
        normalized = re.sub(r"\s+", " ", question.lower()).strip()

        district = self._find_district(normalized)
        crime_type = self._find_crime_type(normalized)

        if not district and not crime_type:
            return None

        if self._is_count_question(normalized):
            return self._count_query(normalized, district, crime_type)

        return self._detail_query(normalized, district, crime_type)

    def _count_query(
        self,
        normalized: str,
        district: str | None,
        crime_type: str | None,
    ) -> SqlPlan:
        where, params = self._where_clause(normalized, district, crime_type)
        sql = f"SELECT COUNT(*) AS total_cases FROM crime_records{where}"
        return SqlPlan(sql=sql, params=params)

    def _detail_query(
        self,
        normalized: str,
        district: str | None,
        crime_type: str | None,
    ) -> SqlPlan:
        where, params = self._where_clause(normalized, district, crime_type)
        sql = (
            "SELECT crime_id, district, police_station, crime_type, crime_date, "
            "crime_time, victim, suspect, vehicle, weapon, status "
            f"FROM crime_records{where} "
            "ORDER BY crime_date DESC LIMIT 50"
        )
        return SqlPlan(sql=sql, params=params)

    def _where_clause(
        self,
        normalized: str,
        district: str | None,
        crime_type: str | None,
    ) -> tuple[str, dict[str, object]]:
        clauses: list[str] = []
        params: dict[str, object] = {}

        if district:
            clauses.append("district = :district")
            params["district"] = district
        if crime_type:
            clauses.append("crime_type = :crime_type")
            params["crime_type"] = crime_type

        month = self._find_month(normalized)
        if month:
            clauses.append("EXTRACT(MONTH FROM crime_date) = :month")
            params["month"] = int(month)
            clauses.append("EXTRACT(YEAR FROM crime_date) = :year")
            params["year"] = self._find_year(normalized) or self.today.year

        months_back = self._find_last_n_months(normalized)
        if months_back:
            clauses.append("crime_date >= :from_date")
            params["from_date"] = self._subtract_months(self.today, months_back)

        if not clauses:
            return "", params
        return " WHERE " + " AND ".join(clauses), params

    @staticmethod
    def _is_count_question(normalized: str) -> bool:
        return any(phrase in normalized for phrase in ["how many", "count", "number of"])

    @staticmethod
    def _find_district(normalized: str) -> str | None:
        for alias, district in DISTRICT_ALIASES.items():
            if alias in normalized:
                return district
        return None

    @staticmethod
    def _find_crime_type(normalized: str) -> str | None:
        for phrase, crime_type in sorted(CRIME_TYPES.items(), key=lambda item: len(item[0]), reverse=True):
            if phrase in normalized:
                return crime_type
        return None

    @staticmethod
    def _find_month(normalized: str) -> str | None:
        for month_name, month_number in MONTHS.items():
            if month_name in normalized:
                return month_number
        return None

    @staticmethod
    def _find_year(normalized: str) -> int | None:
        match = re.search(r"\b(20\d{2})\b", normalized)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    def _find_last_n_months(normalized: str) -> int | None:
        match = re.search(r"last\s+(\d+)\s+months?", normalized)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    def _subtract_months(value: date, months: int) -> date:
        year = value.year
        month = value.month - months
        while month <= 0:
            month += 12
            year -= 1

        days_in_month = [31, 29 if _is_leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        day = min(value.day, days_in_month[month - 1])
        return date(year, month, day)


def _is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
