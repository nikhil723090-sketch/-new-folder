"""Conversation memory backends for context-aware crime chat."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Protocol


@dataclass(frozen=True)
class ChatTurn:
    """One investigator/AI exchange."""

    user_message: str
    ai_answer: str
    sql: str | None
    created_at: str


class ChatMemory(Protocol):
    """Conversation memory interface."""

    def append(self, session_id: str, turn: ChatTurn) -> None:
        """Store one chat turn."""

    def history(self, session_id: str, limit: int = 10) -> list[ChatTurn]:
        """Return recent turns for a session."""


class InMemoryChatMemory:
    """Simple memory for local demos and tests."""

    def __init__(self) -> None:
        self._store: dict[str, list[ChatTurn]] = {}

    def append(self, session_id: str, turn: ChatTurn) -> None:
        self._store.setdefault(session_id, []).append(turn)

    def history(self, session_id: str, limit: int = 10) -> list[ChatTurn]:
        return self._store.get(session_id, [])[-limit:]


class RedisChatMemory:
    """Redis-backed memory for production deployments."""

    def __init__(self, url: str | None = None, ttl_seconds: int = 86400) -> None:
        import redis

        self.client = redis.Redis.from_url(url or os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        self.ttl_seconds = ttl_seconds

    def append(self, session_id: str, turn: ChatTurn) -> None:
        key = _key(session_id)
        self.client.rpush(key, json.dumps(asdict(turn)))
        self.client.expire(key, self.ttl_seconds)

    def history(self, session_id: str, limit: int = 10) -> list[ChatTurn]:
        raw_turns = self.client.lrange(_key(session_id), -limit, -1)
        return [ChatTurn(**json.loads(item)) for item in raw_turns]


def create_turn(user_message: str, ai_answer: str, sql: str | None) -> ChatTurn:
    """Create a timestamped memory turn."""

    return ChatTurn(
        user_message=user_message,
        ai_answer=ai_answer,
        sql=sql,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def build_memory() -> ChatMemory:
    """Choose Redis memory when configured, otherwise use in-memory storage."""

    if os.getenv("CHAT_MEMORY_BACKEND", "memory").lower() == "redis":
        return RedisChatMemory()
    return InMemoryChatMemory()


def _key(session_id: str) -> str:
    return f"scrb:chat:{session_id}"
