# Day 1 Commands

These commands appear in the same order as the Week 1, Day 1 video.

## 1. Create the project

```bash
mkdir -p trexovia-assistant/tests
cd trexovia-assistant

python3 -m venv .venv
source .venv/bin/activate

touch app.py
touch tests/__init__.py
touch tests/test_app.py
touch .gitignore
```

> Windows PowerShell users should activate the virtual environment with `.venv\Scripts\Activate.ps1` instead of `source .venv/bin/activate`.

## 2. Confirm Python

```bash
python --version
```

## 3. Try the response function in Python

```bash
python
```

Then enter:

```python
from app import generate_reply

generate_reply("hello")
generate_reply("Teach me Python")
```

Exit the Python console:

```python
exit()
```

## 4. Run the assistant

```bash
python app.py
```

Type `exit` when you want to stop it.

## 5. Run the automated tests

```bash
python -m unittest discover -s tests -v
```
