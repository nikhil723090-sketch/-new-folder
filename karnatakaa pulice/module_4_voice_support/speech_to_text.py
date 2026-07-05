"""Speech-to-text adapters with Kannada-capable providers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol


class SpeechToTextProvider(Protocol):
    """Provider interface for transcribing audio."""

    name: str

    def transcribe(self, audio_path: str | Path, language: str = "kn") -> str:
        """Return transcript text from an audio file."""


class WhisperSpeechToText:
    """Offline/local transcription using OpenAI Whisper package."""

    name = "whisper"

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or os.getenv("WHISPER_MODEL", "small")

    def transcribe(self, audio_path: str | Path, language: str = "kn") -> str:
        import whisper

        model = whisper.load_model(self.model_name)
        result = model.transcribe(str(audio_path), language=language)
        return result["text"].strip()


class GoogleSpeechToText:
    """Google Speech-to-Text adapter."""

    name = "google"

    def transcribe(self, audio_path: str | Path, language: str = "kn-IN") -> str:
        from google.cloud import speech

        client = speech.SpeechClient()
        content = Path(audio_path).read_bytes()
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code=language,
            enable_automatic_punctuation=True,
        )
        response = client.recognize(config=config, audio=audio)
        return " ".join(result.alternatives[0].transcript for result in response.results).strip()


class AzureSpeechToText:
    """Azure Speech adapter."""

    name = "azure"

    def transcribe(self, audio_path: str | Path, language: str = "kn-IN") -> str:
        import azure.cognitiveservices.speech as speechsdk

        speech_config = speechsdk.SpeechConfig(
            subscription=os.environ["AZURE_SPEECH_KEY"],
            region=os.environ["AZURE_SPEECH_REGION"],
        )
        speech_config.speech_recognition_language = language
        audio_config = speechsdk.AudioConfig(filename=str(audio_path))
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = recognizer.recognize_once()
        return result.text.strip()


def build_stt_provider() -> SpeechToTextProvider:
    """Build configured STT provider."""

    provider = os.getenv("STT_PROVIDER", "whisper").lower()
    if provider == "google":
        return GoogleSpeechToText()
    if provider == "azure":
        return AzureSpeechToText()
    return WhisperSpeechToText()
