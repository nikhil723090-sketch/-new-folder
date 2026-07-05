"""Command-line demo for Module 2 chatbot."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from crime_database.database import SessionLocal
from module_2_ai_chatbot.chatbot import CrimeChatbot


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask the SCRB crime chatbot a question.")
    parser.add_argument("question", help="Natural-language crime database question")
    args = parser.parse_args()

    with SessionLocal() as session:
        result = CrimeChatbot(session).ask(args.question)

    print("Question:", result.question)
    print("Generated SQL:", result.sql)
    print("Source:", result.source)
    print("Answer:", result.answer)


if __name__ == "__main__":
    main()
