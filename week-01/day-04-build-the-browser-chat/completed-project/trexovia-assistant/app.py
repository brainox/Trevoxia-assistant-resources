"""Simple command-line chat assistant for Trexovia.

The assistant responds to a small set of fixed prompts, tracks the conversation
history, and persists that history to disk using the memory module. It is a
minimal rule-based bot intended for local experimentation rather than a
production chat system.
"""

from typing import Callable, Optional

from llm import generate_ai_reply
from memory import add_message, load_history, save_history

RESPONSES = {
    "hello": "Hello, Obinna!",
    "hi": "Hi, Obinna!",
    "help": (
        "I understand hello, hi, help, history, clear, and exit."
    ),
}

CLEAR_COMMANDS = {"clear", "clear history"}
CLEAR_CONFIRMATION = "Conversation history cleared."

History = list[dict[str, str]]
ReplyFunction = Callable[[str, History], str]
SaveFunction = Callable[[History], None]

def find_last_user_message(
    history: list[dict[str, str]],
) -> Optional[str]:
    for message in reversed(history):
        if message["role"] == "user":
            return message["content"]

    return None

def clear_history_if_requested(
    message: str,
    history: History,
) -> bool:
    if message.strip().lower() not in CLEAR_COMMANDS:
        return False
    history.clear()
    return True


def generate_reply(
    message: str,
    history: Optional[list[dict[str, str]]] = None,
    llm_function: Optional[
        Callable[[str, list[dict[str, str]]], str]
    ] = None,
) -> str:
    """Create a reply for the provided user input.

    The response logic is intentionally simple and deterministic. It handles
    blank input, known canned responses, a few "history" queries, and a default
    fallback message for everything else.

    Args:
        message: The raw text entered by the user.
        history: Optional conversation history used to answer history-related
            prompts. When omitted, an empty list is assumed.
        llm_function: Optional function to generate AI replies. When omitted, a default LLM function is used.

    Returns:
        A string response that should be printed to the user.
    """
    if history is None:
        history = []

    cleaned_message = message.strip()
    normalized_message = cleaned_message.lower()

    if not cleaned_message:
        return "Please enter a message."

    if normalized_message in RESPONSES:
        return RESPONSES[normalized_message]

    history_commands = {
        "history",
        "what did i say",
        "what did i say?",
    }

    if normalized_message in history_commands:
        last_message = find_last_user_message(history)

        if last_message:
            return f'Your last message was: "{last_message}"'

        return "You have not sent any previous messages."

    if llm_function is None:
        llm_function = generate_ai_reply

    return llm_function(cleaned_message, history)

def process_message(
    message: str,
    history: History,
    reply_function: ReplyFunction = generate_reply,
    save_function: SaveFunction = save_history,
) -> str:
    if clear_history_if_requested(message, history):  # 1
        save_function(history)
        return CLEAR_CONFIRMATION

    reply = reply_function(message, history)           # 2

    add_message(history, "user", message)              # 3
    add_message(history, "assistant", reply)
    save_function(history)                             # 4

    return reply

def run() -> None:
    """Start the interactive chat loop in the terminal.

    This function loads prior conversation data, prints a startup banner, and then
    repeatedly accepts input until the user types "exit". Each turn stores both
    the user message and the assistant reply so the session can be reconstructed
    later from saved history.
    """
    history = load_history()

    print("Trexovia Assistant")
    print(f"Loaded {len(history)} previous messages.")
    print("Type 'help' for instructions or 'exit' to stop.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        reply = process_message(user_message, history)
        
        print(f"Assistant: {reply}")


if __name__ == "__main__":
    run()