import unittest

from app import clear_history_if_requested, generate_reply


class GenerateReplyTests(unittest.TestCase):
    def test_returns_known_response(self) -> None:
        result = generate_reply("hello")

        self.assertEqual(result, "Hello, Obinna!")

    def test_ignores_capitalization_and_spaces(self) -> None:
        result = generate_reply("  HELP  ")

        self.assertEqual(
            result,
            "I understand hello, hi, help, history, clear history, and exit.",
        )

    def test_uses_llm_for_unknown_message(self) -> None:
        def fake_llm(message: str, history: list) -> str:
            return f"AI reply to: {message}"

        result = generate_reply(
            "Teach me Python",
            llm_function=fake_llm,
        )

        self.assertEqual(result, "AI reply to: Teach me Python")

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

    def test_clear_history_command_empties_memory(self) -> None:
        history = [{"role": "user", "content": "Remember this"}]

        handled = clear_history_if_requested("clear history", history)

        self.assertTrue(handled)
        self.assertEqual(history, [])


if __name__ == "__main__":
    unittest.main()
