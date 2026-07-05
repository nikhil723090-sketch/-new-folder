"""FastAPI endpoint for voice interactions."""

from __future__ import annotations

from pathlib import Path
import sys
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, Form, UploadFile
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from crime_database.database import SessionLocal
from module_4_voice_support.voice_pipeline import VoiceCrimeAssistant


app = FastAPI(title="SCRB Voice Crime Assistant", version="0.1.0")


class VoiceResponse(BaseModel):
    transcript: str
    answer: str
    output_audio_path: str
    resolved_question: str
    sql: str


@app.post("/voice-chat", response_model=VoiceResponse)
async def voice_chat(
    session_id: str = Form(...),
    language: str = Form("kn"),
    audio: UploadFile = File(...),
) -> VoiceResponse:
    """Accept an audio question and return transcript, answer, and audio path."""

    suffix = Path(audio.filename or "question.wav").suffix or ".wav"
    with NamedTemporaryFile(delete=False, suffix=suffix) as uploaded:
        uploaded.write(await audio.read())
        uploaded_path = Path(uploaded.name)

    output_path = uploaded_path.with_name(f"{uploaded_path.stem}_answer.mp3")
    with SessionLocal() as session:
        result = VoiceCrimeAssistant(session).ask_audio(session_id, uploaded_path, output_path, language)

    return VoiceResponse(**result.__dict__)
