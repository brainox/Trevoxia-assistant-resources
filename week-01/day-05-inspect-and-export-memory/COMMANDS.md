# Day 5 Commands

Run these commands from a terminal in the same order used in the lesson.

## 1. Open the evolving application

```bash
cd trexovia-assistant
git pull
source .venv/bin/activate
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Confirm the starting point

```bash
python --version
python -m pip --version
python -m pip install -r requirements.txt
python -m compileall -q app.py llm.py memory.py ui.py tests
python -m unittest discover -s tests -v
```

Expected starting result:

```text
Ran 12 tests

OK
```

## 3. Run checks after the Day 5 changes

```bash
python -m compileall -q app.py llm.py memory.py ui.py tests
python -m unittest discover -s tests -v
```

Expected final result:

```text
Ran 15 tests

OK
```

## 4. Start the browser chat

```bash
python -m streamlit run ui.py
```

Use the sidebar to inspect the saved JSON memory and download the conversation as `trevoxia-conversation.md`.

Stop the server with `Ctrl+C`.

