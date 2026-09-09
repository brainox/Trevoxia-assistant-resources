import os
from typing import Any, Dict, List, Optional


History = List[Dict[str, str]]

SYSTEM_INSTRUCTIONS = (
    "You are Trevoxia Assistant, a friendly and concise AI assistant. "
    "Use the conversation history when it is relevant."
)

MAX_CONTEXT_MESSAGES = 10


def load_environment() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError as error:
        raise RuntimeError(
            "python-dotenv is not installed. "
            "Run: python -m pip install -r requirements.txt"
        ) from error

    load_dotenv()


def build_input(message: str, history: History) -> History:
    recent_history = history[-MAX_CONTEXT_MESSAGES:]

    return [
        *recent_history,
        {
            "role": "user",
            "content": message,
        },
    ]


def generate_ai_reply(
    message: str,
    history: History,
    client: Optional[Any] = None,
    model: Optional[str] = None,
) -> str:
    model_name = model or os.getenv("OPENAI_MODEL")

    if not model_name:
        raise RuntimeError("OPENAI_MODEL is not configured.")

    if client is None:
        try:
            from openai import OpenAI
        except ImportError as error:
            raise RuntimeError(
                "openai is not installed. "
                "Run: python -m pip install -r requirements.txt"
            ) from error

        client = OpenAI()

    response = client.responses.create(
        model=model_name,
        instructions=SYSTEM_INSTRUCTIONS,
        input=build_input(message, history),
        store=False,
    )

    reply = response.output_text.strip()

    if not reply:
        raise RuntimeError("The AI service returned an empty response.")

    return reply
