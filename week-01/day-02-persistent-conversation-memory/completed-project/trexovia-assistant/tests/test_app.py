import unittest

from app import generate_reply


class GenerateReplyTests(unittest.TestCase):
    def test_returns_known_response(self) -> None:
        result = generate_reply("hello")

        self.assertEqual(result, "Hello, Obinna!")

    def test_ignores_capitalization_and_spaces(self) -> None:
        result = generate_reply("  HELP  ")

        self.assertEqual(
            result,
            "I understand hello, hi, help, history, and exit.",
        )

    def test_returns_fallback_response(self) -> None:
        result = generate_reply("Teach me Python")

        self.assertEqual(result, "You said: Teach me Python")

    def test_rejects_empty_message(self) -> None:
        result = generate_reply("   ")

        self.assertEqual(result, "Please enter a message.")

    def test_returns_last_user_message(self) -> None:
        history = [
            {"role": "user", "content": "I am learning Python"},
            {"role": "assistant", "content": "That is great."},
        ]

        result = generate_reply("history", history)

        self.assertEqual(
            result,
            'Your last message was: "I am learning Python"',
        )


if __name__ == "__main__":
    unittest.main()
