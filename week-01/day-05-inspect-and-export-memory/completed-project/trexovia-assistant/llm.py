import os
from typing import Any, Optional
from dotenv import load_dotenv

load_dotenv()

SYSTEM_INSTRUCTIONS = (
    "You are Trevoxia Assistant, a friendly and concise AI assistant. "
    "Use the conversation history when it is relevant."
)

MAX_CONTEXT_MESSAGES = 10


def build_input(
    message: str,
    history: list[dict[str, str]],
) -> list[dict[str, str]]:
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
    history: list[dict[str, str]],
    client: Optional[Any] = None,
    model: Optional[str] = None,
) -> str:
    model_name = model or os.getenv("OPENAI_MODEL")

    if not model_name:
        raise RuntimeError("OPENAI_MODEL is not configured.")

    if client is None:
        from openai import OpenAI

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