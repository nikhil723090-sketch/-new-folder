"""Audit logging helpers."""

from __future__ import annotations

from sqlalchemy.orm import Session

from .models import AuditLog


class AuditLogger:
    """Write compliance audit records."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def log(
        self,
        *,
        user_id: str,
        role: str,
        action: str,
        question: str | None = None,
        ai_response: str | None = None,
        generated_sql: str | None = None,
        prediction: str | None = None,
    ) -> AuditLog:
        entry = AuditLog(
            user_id=user_id,
            role=role,
            action=action,
            question=question,
            ai_response=ai_response,
            generated_sql=generated_sql,
            prediction=prediction,
        )
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry
