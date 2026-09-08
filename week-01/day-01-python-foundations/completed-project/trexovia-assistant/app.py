RESPONSES = {
    "hello": "Hello, Obinna!",
    "hi": "Hi, Obinna!",
    "help": "I understand hello, hi, help, and exit.",
}


def generate_reply(message: str) -> str:
    cleaned_message = message.strip()
    normalized_message = cleaned_message.lower()

    if not cleaned_message:
        return "Please enter a message."

    if normalized_message in RESPONSES:
        return RESPONSES[normalized_message]

    return f"You said: {cleaned_message}"

def run() -> None:
    print("Trexovia Assistant")
    print("Type 'help' for instructions or 'exit' to stop.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "exit":
            print("Assistant: Goodbye!")
            break

        reply = generate_reply(user_message)
        print(f"Assistant: {reply}")


if __name__ == "__main__":
    run()
