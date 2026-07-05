"""FastAPI endpoint for context-aware chat."""

from __future__ import annotations

from pathlib import Path
import sys

from fastapi import FastAPI
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from crime_database.database import SessionLocal
from module_3_context_chat.context_chatbot import ContextAwareCrimeChatbot


app = FastAPI(title="SCRB Context-Aware Crime Chat", version="0.1.0")


class ContextChatRequest(BaseModel):
    session_id: str
    question: str


class ContextChatResponse(BaseModel):
    session_id: str
    original_question: str
    resolved_question: str
    sql: str
    answer: str
    source: str
    rows: list[dict]


@app.post("/context-chat", response_model=ContextChatResponse)
def context_chat(request: ContextChatRequest) -> ContextChatResponse:
    """Answer a question using conversation memory."""

    with SessionLocal() as session:
        result = ContextAwareCrimeChatbot(session).ask(request.session_id, request.question)

    return ContextChatResponse(**result.__dict__)
