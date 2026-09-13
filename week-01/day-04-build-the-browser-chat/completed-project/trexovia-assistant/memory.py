"""Simple file-backed conversation history utilities.

This module provides tiny helpers to load, update (in-memory), and save a
conversation history stored as JSON on disk. The expected JSON format is a
list of message objects, where each message is a mapping with string keys
"role" and "content", for example:

    [
      {"role": "user", "content": "Hello"},
      {"role": "assistant", "content": "Hi!"}
    ]

The functions keep behaviour minimal and intentionally do not provide
concurrency control or atomic writes. Callers should handle exceptions from
I/O and JSON parsing as appropriate for their application.

Module-level constants
- DEFAULT_HISTORY_PATH: default file path used by load_history/save_history.

This file uses PEP 257-compatible docstrings and conservative inline
comments to make maintenance straightforward.
"""

from __future__ import annotations

import json
from pathlib import Path


DEFAULT_HISTORY_PATH = Path("data/history.json")
"""
Default file path for conversation history.

This is a relative path by design; callers may pass an explicit Path to
load_history/save_history to change where history is read from or written
to.
"""


def load_history(path: Path = DEFAULT_HISTORY_PATH) -> list[dict[str, str]]:
    """Load conversation history from a JSON file.

    If the file does not exist, an empty list is returned. If the file
    exists but does not contain a top-level JSON list, a ValueError is
    raised. JSON decoding and I/O errors are propagated to the caller.

    Args:
        path: Path to the JSON file that stores the history. Defaults to
            DEFAULT_HISTORY_PATH.

    Returns:
        A list of message dictionaries. Each message is expected to have
        the keys "role" and "content" (this function does not validate
        the shape of each message beyond confirming the top-level is a
        list).

    Raises:
        ValueError: If the file contains JSON that is not a list.
        json.JSONDecodeError: If the file contains invalid JSON.
        OSError: For errors opening/reading the file.
    """
    # If the history file is not present, return an empty conversation.
    if not path.exists():
        return []

    # Read and parse the JSON file using UTF-8 encoding for portability.
    with path.open("r", encoding="utf-8") as file:
        history = json.load(file)

    # Ensure the top-level JSON structure is a list (expected format).
    if not isinstance(history, list):
        raise ValueError("Conversation history must be a list.")

    return history


def add_message(history: list[dict[str, str]], role: str, content: str) -> None:
    """Append a message to an in-memory history list.

    This function mutates the provided `history` list in place.

    Args:
        history: The in-memory list of message dictionaries to append to.
        role: The sender role, e.g. "user" or "assistant".
        content: The textual content of the message.

    Returns:
        None

    Notes:
        - No validation is performed on the message beyond constructing the
          expected mapping. If stricter validation is required, validate
          before calling this helper.
    """
    history.append({"role": role, "content": content})


def save_history(history: list[dict[str, str]], path: Path = DEFAULT_HISTORY_PATH) -> None:
    """Persist the in-memory history to disk as JSON.

    The parent directory of `path` is created if it does not exist. The
    file is written using UTF-8 encoding and formatted with an indentation
    of 2 spaces to remain human readable.

    Args:
        history: The list of message dictionaries to persist.
        path: Path where the history should be written. Defaults to
            DEFAULT_HISTORY_PATH.

    Returns:
        None

    Raises:
        TypeError: If `history` contains objects that are not JSON
            serializable.
        OSError: For errors creating directories or writing the file.

    Notes:
        - Writes are not atomic. A crash during write may leave a
          partially-written file. For applications that require stronger
          durability guarantees, consider writing to a temporary file and
          performing an atomic replace (os.replace) or using file locking.
        - This function does not provide concurrency control. If multiple
          processes may write the same file concurrently, use an external
          lock or a different persistence mechanism.
    """
    # Ensure the parent directory exists (no-op if it already does).
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write the JSON file in a straightforward, human-readable form.
    with path.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)
