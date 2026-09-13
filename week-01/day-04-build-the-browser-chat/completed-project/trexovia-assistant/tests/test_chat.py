import unittest

from app import (
    CLEAR_CONFIRMATION,
    clear_history_if_requested,
    process_message,
)


class ChatWorkflowTests(unittest.TestCase):

    def test_clear_history_if_requested_recognizes_command(self) -> None:
        history = [{"role": "user", "content": "Remember this"}]  # 1

        handled = clear_history_if_requested(
            "  CLEAR HISTORY  ",
            history,
        )                                                        # 2

        self.assertTrue(handled)
        self.assertEqual(history, [])                            # 3

    def test_process_message_saves_complete_turn(self) -> None:
        history = []
        saved_snapshots = []                              # 1

        def fake_reply(message: str, current_history: list) -> str:
            return "An API connects software systems."    # 2

        def fake_save(current_history: list) -> None:
            saved_snapshots.append(list(current_history)) # 3

        reply = process_message(
            "Teach me APIs",
            history,
            reply_function=fake_reply,
            save_function=fake_save,
        )

        self.assertEqual(reply, "An API connects software systems.")
        self.assertEqual(len(history), 2)
        self.assertEqual(saved_snapshots, [history])       # 4

    def test_process_message_clears_and_saves_history(self) -> None:
        history = [{"role": "user", "content": "Private message"}]
        saved_snapshots = []

        def fake_save(current_history: list) -> None:
            saved_snapshots.append(list(current_history))

        reply = process_message(
            "clear",
            history,
            save_function=fake_save,
        )

        self.assertEqual(reply, CLEAR_CONFIRMATION)  # 1
        self.assertEqual(history, [])                # 2
        self.assertEqual(saved_snapshots, [[]])      # 3