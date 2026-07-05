"""Module 3: context-aware chat with conversation memory."""

__all__ = ["ContextAwareCrimeChatbot"]


def __getattr__(name: str):
    if name == "ContextAwareCrimeChatbot":
        from .context_chatbot import ContextAwareCrimeChatbot

        return ContextAwareCrimeChatbot
    raise AttributeError(name)
