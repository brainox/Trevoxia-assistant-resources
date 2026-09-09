# Day 2 Commands

These commands appear in the same order as the Week 1, Day 2 tutorial.

## 1. Open the project

```bash
cd trexovia-assistant
source .venv/bin/activate
```

> Windows PowerShell: `.venv\Scripts\Activate.ps1`

## 2. Create the memory files

```bash
touch memory.py tests/test_memory.py
mkdir -p data
```

## 3. Verify the default path

```bash
python -c "from memory import DEFAULT_HISTORY_PATH; print(DEFAULT_HISTORY_PATH)"
```

## 4. Verify a missing history file

```bash
python -c "from memory import load_history; print(load_history())"
```

## 5. Save and inspect one message

```bash
python -c "from memory import add_message, save_history; h=[]; add_message(h, 'user', 'Hello'); save_history(h)"
python -m json.tool data/history.json
```

## 6. Compile and test

```bash
python -m compileall -q app.py memory.py tests
python -m unittest discover -s tests -v
```

## 7. Run the assistant

```bash
python app.py
```

Send one message, type `exit`, restart the program, and enter `history`.
