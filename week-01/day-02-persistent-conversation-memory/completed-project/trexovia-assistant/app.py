from typing import Dict, List, Optional

from memory import add_message, load_history, save_history


History = List[Dict[str, str]]

RESPONSES = {
    "hello": "Hello, Obinna!",
    "hi": "Hi, Obinna!",
    "help": "I understand hello, hi, help, history, and exit.",
}

HISTORY_COMMANDS = {
    "history",
    "what did i say",
    "what did i say?",
}


def find_last_user_message(history: History) -> Optional[str]:
    for message in reversed(history):
        if message["role"] == "user":
            return message["content"]

    return None


def generate_reply(
    message: str,
    history: Optional[History] = None,
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

    return f"You said: {cleaned_message}"


def run() -> None:
    history = load_history()

    print("Trevoxia Assistant")
    print(f"Loaded {len(history)} previous messages.")
    print("Type 'help' for instructions or 'exit' to stop.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        reply = generate_reply(user_message, history)
        print(f"Assistant: {reply}")

        add_message(history, "user", user_message)
        add_message(history, "assistant", reply)
        save_history(history)


if __name__ == "__main__":
    run()
