"""Module 2: AI chatbot for natural-language crime database queries."""

__all__ = ["CrimeChatbot"]


def __getattr__(name: str):
    if name == "CrimeChatbot":
        from .chatbot import CrimeChatbot

        return CrimeChatbot
    raise AttributeError(name)
