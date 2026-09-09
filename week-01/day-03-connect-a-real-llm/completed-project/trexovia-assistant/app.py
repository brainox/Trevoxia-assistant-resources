from typing import Callable, Dict, List, Optional

from llm import generate_ai_reply, load_environment
from memory import add_message, load_history, save_history


History = List[Dict[str, str]]
LLMFunction = Callable[[str, History], str]

RESPONSES = {
    "hello": "Hello, Obinna!",
    "hi": "Hi, Obinna!",
    "help": (
        "I understand hello, hi, help, history, clear history, and exit."
    ),
}

HISTORY_COMMANDS = {
    "history",
    "what did i say",
    "what did i say?",
}

CLEAR_HISTORY_COMMANDS = {
    "clear history",
    "clear memory",
}


def find_last_user_message(history: History) -> Optional[str]:
    for message in reversed(history):
        if message["role"] == "user":
            return message["content"]

    return None


def clear_history_if_requested(message: str, history: History) -> bool:
    if message.strip().lower() not in CLEAR_HISTORY_COMMANDS:
        return False

    history.clear()
    return True


def generate_reply(
    message: str,
    history: Optional[History] = None,
    llm_function: Optional[LLMFunction] = None,
) -> str:
    if history is None:
        history = []

    cleaned_message = message.strip()
    normalized_message = cleaned_message.lower()

    if not cleaned_message:
        return "Please enter a message."

    if normalized_message in RESPONSES:
        return RESPONSES[normalized_message]

    if normalized_message in HISTORY_COMMANDS:
        last_message = find_last_user_message(history)

        if last_message:
            return f'Your last message was: "{last_message}"'

        return "You have not sent any previous messages."

    if llm_function is None:
        llm_function = generate_ai_reply

    return llm_function(cleaned_message, history)


def run() -> None:
    load_environment()
    history = load_history()

    print("Trevoxia Assistant")
    print(f"Loaded {len(history)} previous messages.")
    print("Type 'help' for instructions or 'exit' to stop.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        if clear_history_if_requested(user_message, history):
            save_history(history)
            print("Assistant: Conversation history cleared.")
            continue

        try:
            reply = generate_reply(user_message, history)
        except Exception as error:
            print("Assistant: I could not reach the AI service.")
            print(f"Details: {error}")
            continue

        print(f"Assistant: {reply}")

        add_message(history, "user", user_message)
        add_message(history, "assistant", reply)
        save_history(history)


if __name__ == "__main__":
    run()
