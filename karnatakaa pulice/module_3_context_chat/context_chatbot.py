"""Context-aware chatbot that remembers earlier investigation questions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from module_2_ai_chatbot.chatbot import CrimeChatbot

from .context_resolver import resolve_follow_up
from .memory import ChatMemory, build_memory, create_turn


@dataclass(frozen=True)
class ContextChatbotResult:
    """Result from one context-aware chat turn."""

    session_id: str
    original_question: str
    resolved_question: str
    sql: str
    rows: list[dict[str, Any]]
    answer: str
    source: str


class ContextAwareCrimeChatbot:
    """Add conversation memory and follow-up resolution to Module 2."""

    def __init__(self, session: Session, memory: ChatMemory | None = None) -> None:
        self.session = session
        self.memory = memory or build_memory()
        self.chatbot = CrimeChatbot(session)

    def ask(self, session_id: str, question: str) -> ContextChatbotResult:
        """Answer using previous turns from the same session."""

        history = self.memory.history(session_id)
        resolved_question = resolve_follow_up(question, history)
        result = self.chatbot.ask(resolved_question)

        self.memory.append(session_id, create_turn(question, result.answer, result.sql))

        return ContextChatbotResult(
            session_id=session_id,
            original_question=question,
            resolved_question=resolved_question,
            sql=result.sql,
            rows=result.rows,
            answer=result.answer,
            source=result.source,
        )
