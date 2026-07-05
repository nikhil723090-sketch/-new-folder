"""Module 4: voice support for speech-to-text and text-to-speech."""

__all__ = ["VoiceCrimeAssistant"]


def __getattr__(name: str):
    if name == "VoiceCrimeAssistant":
        from .voice_pipeline import VoiceCrimeAssistant

        return VoiceCrimeAssistant
    raise AttributeError(name)
