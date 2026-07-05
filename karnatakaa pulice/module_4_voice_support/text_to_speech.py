"""Text-to-speech adapters with Kannada-capable providers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol


class TextToSpeechProvider(Protocol):
    """Provider interface for creating spoken audio."""

    name: str

    def synthesize(self, text: str, output_path: str | Path, language: str = "kn") -> Path:
        """Create an audio file and return its path."""


class GttsTextToSpeech:
    """Simple TTS using gTTS."""

    name = "gtts"

    def synthesize(self, text: str, output_path: str | Path, language: str = "kn") -> Path:
        from gtts import gTTS

        output = Path(output_path)
        tts = gTTS(text=text, lang=language)
        tts.save(str(output))
        return output


class AzureTextToSpeech:
    """Azure neural TTS adapter."""

    name = "azure"

    def synthesize(self, text: str, output_path: str | Path, language: str = "kn-IN") -> Path:
        import azure.cognitiveservices.speech as speechsdk

        output = Path(output_path)
        speech_config = speechsdk.SpeechConfig(
            subscription=os.environ["AZURE_SPEECH_KEY"],
            region=os.environ["AZURE_SPEECH_REGION"],
        )
        speech_config.speech_synthesis_language = language
        speech_config.speech_synthesis_voice_name = os.getenv("AZURE_TTS_VOICE", "kn-IN-SapnaNeural")
        audio_config = speechsdk.audio.AudioOutputConfig(filename=str(output))
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        synthesizer.speak_text_async(text).get()
        return output


def build_tts_provider() -> TextToSpeechProvider:
    """Build configured TTS provider."""

    provider = os.getenv("TTS_PROVIDER", "gtts").lower()
    if provider == "azure":
        return AzureTextToSpeech()
    return GttsTextToSpeech()
