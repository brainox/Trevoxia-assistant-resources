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
            "I understand hello, hi, help, and exit.",
        )

    def test_returns_fallback_response(self) -> None:
        result = generate_reply("Teach me Python")

        self.assertEqual(result, "You said: Teach me Python")

    def test_rejects_empty_message(self) -> None:
        result = generate_reply("   ")

        self.assertEqual(result, "Please enter a message.")


if __name__ == "__main__":
    unittest.main()
