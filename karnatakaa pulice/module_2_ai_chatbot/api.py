"""FastAPI endpoint for the AI chatbot module."""

from __future__ import annotations

from pathlib import Path
import sys

from fastapi import FastAPI
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from crime_database.database import SessionLocal
from module_2_ai_chatbot.chatbot import CrimeChatbot


app = FastAPI(title="SCRB Crime AI Chatbot", version="0.1.0")


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    sql: str
    answer: str
    source: str
    rows: list[dict]


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Ask the chatbot a natural-language crime database question."""

    with SessionLocal() as session:
        result = CrimeChatbot(session).ask(request.question)

    return ChatResponse(
        question=result.question,
        sql=result.sql,
        answer=result.answer,
        source=result.source,
        rows=result.rows,
    )
