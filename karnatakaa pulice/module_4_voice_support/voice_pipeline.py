"""Voice pipeline: audio in, chatbot answer, audio out."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from module_3_context_chat.context_chatbot import ContextAwareCrimeChatbot

from .speech_to_text import SpeechToTextProvider, build_stt_provider
from .text_to_speech import TextToSpeechProvider, build_tts_provider


@dataclass(frozen=True)
class VoiceAssistantResult:
    """Result of a voice interaction."""

    transcript: str
    answer: str
    output_audio_path: str
    resolved_question: str
    sql: str


class VoiceCrimeAssistant:
    """Connect STT, context-aware chatbot, and TTS."""

    def __init__(
        self,
        session: Session,
        stt_provider: SpeechToTextProvider | None = None,
        tts_provider: TextToSpeechProvider | None = None,
    ) -> None:
        self.chatbot = ContextAwareCrimeChatbot(session)
        self.stt_provider = stt_provider or build_stt_provider()
        self.tts_provider = tts_provider or build_tts_provider()

    def ask_audio(
        self,
        session_id: str,
        audio_path: str | Path,
        output_audio_path: str | Path,
        language: str = "kn",
    ) -> VoiceAssistantResult:
        """Transcribe audio, ask chatbot, synthesize answer."""

        transcript = self.stt_provider.transcribe(audio_path, language=language)
        chat_result = self.chatbot.ask(session_id, transcript)
        output = self.tts_provider.synthesize(chat_result.answer, output_audio_path, language=language)

        return VoiceAssistantResult(
            transcript=transcript,
            answer=chat_result.answer,
            output_audio_path=str(output),
            resolved_question=chat_result.resolved_question,
            sql=chat_result.sql,
        )
