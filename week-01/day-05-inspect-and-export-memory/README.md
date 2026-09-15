# Week 1, Day 5 — Inspect and Export Conversation Memory

Today we make the assistant's memory visible, measurable, and portable.

The application already stores every conversation in JSON. By the end of this lesson, people using the browser chat can inspect that saved data and download a readable Markdown transcript.

## Yesterday's starting point

Day 4 gave us one tested chat workflow used by both interfaces:

- `app.py` owns message processing.
- `memory.py` loads and saves JSON history.
- `ui.py` renders the Streamlit browser chat.
- The sidebar can count messages and clear history.
- Twelve automated tests pass.

Start from application commit [`b76f8a0`](https://github.com/brainox/trexovia-assistant/commit/b76f8a08985ed92afd3852b02a8b18ee27510e36).

## Today's objective

Add memory tools that let a user:

- Count user and assistant messages through reusable Python logic.
- Inspect the raw saved memory inside the browser.
- Convert a conversation into readable Markdown.
- Download that Markdown transcript.
- Keep existing history unchanged when the AI provider fails.
- Prove all behavior with offline automated tests.

Estimated time: **75 minutes**

## Mental model

```text
data/history.json
       |
       v
 Python history list
    /        \
   v          v
Inspect JSON  Format Markdown
                  |
                  v
          Download transcript
```

JSON remains the application's storage format. Markdown is only an export format for people to read or share.

## Session 1 — Verify the Day 4 baseline

Time: **10 minutes**

Open the evolving application and activate its virtual environment:

```bash
cd trexovia-assistant
git pull
source .venv/bin/activate
```

Install dependencies and run the existing checks:

```bash
python -m pip install -r requirements.txt
python -m compileall -q app.py llm.py memory.py ui.py tests
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 12 tests

OK
```

Checkpoint: fix any baseline failure before adding Day 5 behavior.

## Session 2 — Move message counting into the memory module

Time: **15 minutes**

The sidebar currently calculates counts itself. Counting saved messages is memory logic, so place it in `memory.py`. This keeps the interface focused on presentation and makes the logic easy to test.

Add this function below `add_message()`:

```python
def count_messages(
    history: list[dict[str, str]],
    role: str,
) -> int:
    return sum(
        1
        for message in history
        if message["role"] == role
    )
```

How it works:

1. The function receives the full history and the role we want to count.
2. It visits each message.
3. A matching role contributes `1`; every other message contributes nothing.
4. `sum()` returns the total.

Add `count_messages` to the import in `ui.py`:

```python
from memory import (
    count_messages,
    format_history_as_markdown,
    load_history,
)
```

Then replace the sidebar's inline counting with:

```python
user_count = count_messages(history, "user")
assistant_count = count_messages(history, "assistant")
```

We will add `format_history_as_markdown` in the next session. Your editor may show an unresolved import until then.

### Test the count helper

Import `count_messages` in `tests/test_memory.py`, then add:

```python
def test_counts_messages_for_one_role(self) -> None:
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
        {"role": "user", "content": "Help me plan."},
    ]

    self.assertEqual(count_messages(history, "user"), 2)
    self.assertEqual(count_messages(history, "assistant"), 1)
```

Checkpoint: the helper counts each role without changing `history`.

## Session 3 — Convert memory into Markdown

Time: **20 minutes**

Add these labels near `DEFAULT_HISTORY_PATH` in `memory.py`:

```python
ROLE_LABELS = {
    "user": "You",
    "assistant": "Trevoxia",
}
```

Now add the formatter below `count_messages()`:

```python
def format_history_as_markdown(
    history: list[dict[str, str]],
) -> str:
    lines = ["# Trevoxia Conversation", ""]  # 1

    if not history:
        lines.append("No messages yet.")       # 2

    for message in history:
        label = ROLE_LABELS.get(               # 3
            message["role"],
            message["role"].title(),
        )
        lines.extend([                         # 4
            f"## {label}",
            message["content"],
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"  # 5
```

Numbered explanation:

1. Start the document with one title and a blank line.
2. Give an empty conversation a useful message instead of an empty file.
3. Convert internal roles into human-friendly labels. Unknown roles still receive a readable title.
4. Add a heading, the message content, and spacing for every saved message.
5. Join the pieces and guarantee exactly one newline at the end.

### Test the Markdown formatter

Import `format_history_as_markdown` in `tests/test_memory.py`, then add:

```python
def test_formats_history_as_markdown(self) -> None:
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
    ]

    result = format_history_as_markdown(history)

    self.assertEqual(
        result,
        (
            "# Trevoxia Conversation\n\n"
            "## You\nHello\n\n"
            "## Trevoxia\nHi!\n"
        ),
    )
```

Checkpoint: storage is still JSON; the new function only returns a Markdown string.

## Session 4 — Inspect saved memory in Streamlit

Time: **10 minutes**

Inside the `with st.sidebar:` block in `ui.py`, add an expander below the message counts:

```python
with st.expander("Inspect saved memory"):
    st.json(history)
```

The expander keeps technical details out of the way until a learner needs them. `st.json()` renders the Python list as structured data, making the relationship between the screen and `data/history.json` easy to see.

Checkpoint:

1. Run `python -m streamlit run ui.py`.
2. Send one message.
3. Expand **Inspect saved memory**.
4. Confirm you see one `user` item and one `assistant` item.

## Session 5 — Download the conversation

Time: **10 minutes**

Add this button below the inspector and above **Clear history**:

```python
st.download_button(
    "Download conversation",
    data=format_history_as_markdown(history),
    file_name="trevoxia-conversation.md",
    mime="text/markdown",
    use_container_width=True,
)
```

What each value controls:

1. The first string is the button label.
2. `data` is created from the current in-memory conversation.
3. `file_name` gives the downloaded file a predictable name.
4. `mime` tells the browser that the content is Markdown text.

Checkpoint: download the file and open it in your editor. It should contain headings for **You** and **Trevoxia**, followed by the message text.

## Session 6 — Protect memory when a reply fails

Time: **5 minutes**

`process_message()` already asks the AI for a reply before it appends or saves the new turn. Add a regression test so a future refactor cannot accidentally save half a conversation.

Add this test to `tests/test_chat.py`:

```python
def test_failed_reply_does_not_change_or_save_history(self) -> None:
    history = [
        {"role": "user", "content": "Existing message"},
    ]
    saved_snapshots = []

    def failing_reply(message: str, current_history: list) -> str:
        raise RuntimeError("AI service unavailable")

    def fake_save(current_history: list) -> None:
        saved_snapshots.append(list(current_history))

    with self.assertRaises(RuntimeError):
        process_message(
            "New message",
            history,
            reply_function=failing_reply,
            save_function=fake_save,
        )

    self.assertEqual(
        history,
        [{"role": "user", "content": "Existing message"}],
    )
    self.assertEqual(saved_snapshots, [])
```

The test proves two important guarantees:

- A failed AI request does not append the new user message.
- A failed AI request does not write anything to disk.

The terminal's `try` block should cover only `process_message()`, followed by printing the reply after the error handler:

```python
try:
    reply = process_message(user_message, history)
except Exception as error:
    print(f"Assistant: I could not generate a response: {error}")
    print(f"Details: {error}")
    continue

print(f"Assistant: {reply}")
```

## Session 7 — Run the final checks

Time: **5 minutes**

```bash
python -m compileall -q app.py llm.py memory.py ui.py tests
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 15 tests

OK
```

Start the browser interface:

```bash
python -m streamlit run ui.py
```

## Final project structure

```text
trexovia-assistant/
├── app.py
├── llm.py
├── memory.py
├── requirements.txt
├── ui.py
└── tests/
    ├── __init__.py
    ├── test_app.py
    ├── test_chat.py
    ├── test_llm.py
    └── test_memory.py
```

## Common mistakes

- **Changing the JSON file into Markdown:** keep JSON for storage; generate Markdown only when downloading.
- **Counting messages in `ui.py`:** import and reuse `count_messages()` so the rule stays testable.
- **Using `history.count("user")`:** each history item is a dictionary, not a role string.
- **Saving before the AI reply succeeds:** this can leave an unmatched user message in memory.
- **Forgetting the MIME type:** use `text/markdown` for the download.
- **Testing against the live API:** the lesson's automated tests use fake functions and require no network call.

## Completion checklist

- [ ] The sidebar shows user and assistant message counts.
- [ ] Saved JSON memory can be expanded and inspected.
- [ ] The conversation downloads as `trevoxia-conversation.md`.
- [ ] The downloaded transcript uses readable role headings.
- [ ] A failed AI reply leaves history unchanged.
- [ ] All 15 tests pass.
- [ ] The browser chat still sends, remembers, reloads, and clears messages.

## Completed project

The exact final files are in [`completed-project/trexovia-assistant`](completed-project/trexovia-assistant).

The matching application commit is [`85c1e0c`](https://github.com/brainox/trexovia-assistant/commit/85c1e0c8905af7b969058c72db4ee6ef6db5a8bb).

## End-of-day report

```text
Completed:
Test result:
What I learned about storage versus export formats:
One thing I inspected in the saved JSON:
Blocker:
Time spent:
```

Today's working software makes its memory transparent and gives users ownership of their conversation data through a readable download.
