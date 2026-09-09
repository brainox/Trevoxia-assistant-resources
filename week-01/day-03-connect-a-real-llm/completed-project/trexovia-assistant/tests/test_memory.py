import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from memory import add_message, load_history, save_history


class MemoryTests(unittest.TestCase):
    def test_missing_file_returns_empty_history(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"

            self.assertEqual(load_history(path), [])

    def test_saves_and_loads_messages(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "history.json"
            history = []

            add_message(history, "user", "Hello")
            add_message(history, "assistant", "Hi!")
            save_history(history, path)

            self.assertEqual(load_history(path), history)


if __name__ == "__main__":
    unittest.main()
