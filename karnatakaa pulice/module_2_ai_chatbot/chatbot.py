"""End-to-end chatbot pipeline for natural-language crime queries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from .llm_providers import LLMProvider, build_llm_provider
from .nl_to_sql import RuleBasedSqlPlanner
from .response_formatter import format_answer
from .sql_safety import ensure_safe_select


@dataclass(frozen=True)
class ChatbotResult:
    """Structured output from one chatbot turn."""

    question: str
    sql: str
    rows: list[dict[str, Any]]
    answer: str
    source: str


class CrimeChatbot:
    """Convert investigator questions into SQL and readable answers."""

    def __init__(self, session: Session, llm_provider: LLMProvider | None = None) -> None:
        self.session = session
        self.rule_planner = RuleBasedSqlPlanner()
        self.llm_provider = llm_provider or build_llm_provider()

    def ask(self, question: str) -> ChatbotResult:
        """Answer a crime database question."""

        planned = self.rule_planner.plan(question)
        source = "rule-based"

        if planned is None:
            planned = self.llm_provider.generate_sql(question)
            source = self.llm_provider.name

        sql = ensure_safe_select(planned.sql)
        rows = [dict(row._mapping) for row in self.session.execute(text(sql), planned.params)]
        answer = format_answer(question=question, sql=sql, rows=rows)

        return ChatbotResult(
            question=question,
            sql=sql,
            rows=rows,
            answer=answer,
            source=source,
        )
