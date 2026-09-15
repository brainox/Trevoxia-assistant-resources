import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from memory import (
    add_message,
    count_messages,
    format_history_as_markdown,
    load_history,
    save_history,
)


class MemoryTests(unittest.TestCase):
    def test_missing_file_returns_empty_history(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"

            self.assertEqual(load_history(path), [])

    def test_saves_and_loads_messages(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "history.json"
            history: list[dict[str, str]] = []

            add_message(history, "user", "Hello")
            add_message(history, "assistant", "Hi!")
            save_history(history, path)

            loaded_history = load_history(path)

            self.assertEqual(loaded_history, history)

    def test_counts_messages_for_one_role(self) -> None:
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"},
            {"role": "user", "content": "Help me plan."},
        ]

        self.assertEqual(count_messages(history, "user"), 2)       # 1
        self.assertEqual(count_messages(history, "assistant"), 1)  # 2

    def test_formats_history_as_markdown(self) -> None:
        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"},
        ]

        result = format_history_as_markdown(history)

        self.assertEqual(
            result,
            (
                "# Trevoxia Conversation\n\n"  # 1
                "## You\nHello\n\n"            # 2
                "## Trevoxia\nHi!\n"           # 3
            ),
        )

if __name__ == "__main__":
    unittest.main()