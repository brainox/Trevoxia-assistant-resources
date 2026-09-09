import json
from pathlib import Path
from typing import Dict, List


History = List[Dict[str, str]]
DEFAULT_HISTORY_PATH = Path("data/history.json")


def load_history(path: Path = DEFAULT_HISTORY_PATH) -> History:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        history = json.load(file)

    if not isinstance(history, list):
        raise ValueError("Conversation history must be a list.")

    return history


def add_message(
    history: History,
    role: str,
    content: str,
) -> None:
    history.append({
        "role": role,
        "content": content,
    })


def save_history(
    history: History,
    path: Path = DEFAULT_HISTORY_PATH,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)
