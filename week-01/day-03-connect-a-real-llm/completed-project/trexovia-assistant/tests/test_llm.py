import unittest
from types import SimpleNamespace

from llm import MAX_CONTEXT_MESSAGES, build_input, generate_ai_reply


class FakeResponses:
    def __init__(self) -> None:
        self.last_request = {}

    def create(self, **kwargs: object) -> SimpleNamespace:
        self.last_request = kwargs
        return SimpleNamespace(output_text="Mock AI response")


class FakeClient:
    def __init__(self) -> None:
        self.responses = FakeResponses()


class LLMTests(unittest.TestCase):
    def test_build_input_keeps_recent_history(self) -> None:
        history = [
            {"role": "user", "content": f"Message {index}"}
            for index in range(MAX_CONTEXT_MESSAGES + 2)
        ]

        result = build_input("Current question", history)

        self.assertEqual(len(result), MAX_CONTEXT_MESSAGES + 1)
        self.assertEqual(result[0]["content"], "Message 2")
        self.assertEqual(result[-1]["content"], "Current question")

    def test_generate_ai_reply_uses_responses_api(self) -> None:
        client = FakeClient()

        result = generate_ai_reply(
            "Explain APIs",
            [],
            client=client,
            model="test-model",
        )

        self.assertEqual(result, "Mock AI response")
        self.assertEqual(
            client.responses.last_request["model"],
            "test-model",
        )
        self.assertFalse(client.responses.last_request["store"])


if __name__ == "__main__":
    unittest.main()
