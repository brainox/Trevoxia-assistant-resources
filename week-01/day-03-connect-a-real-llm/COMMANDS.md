# Day 3 Commands

These commands appear in the same order as the Week 1, Day 3 tutorial.

## 1. Open the project and verify Python

```bash
cd trexovia-assistant
source .venv/bin/activate
python --version
python -c "import sys; print(sys.executable)"
python -m pip --version
```

> Windows PowerShell: `.venv\Scripts\Activate.ps1`

## 2. Create the new files

```bash
touch llm.py tests/test_llm.py requirements.txt .env.example
```

## 3. Install dependencies

```bash
python -m pip install -r requirements.txt
python -c "import openai, dotenv; print('Dependencies imported successfully')"
```

## 4. Create local configuration

```bash
cp .env.example .env
```

Edit `.env`, then verify without printing the key:

```bash
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Key:', bool(os.getenv('OPENAI_API_KEY'))); print('Model:', bool(os.getenv('OPENAI_MODEL')))"
```

## 5. Compile and run offline tests

```bash
python -m compileall -q app.py llm.py memory.py tests
python -m unittest discover -s tests -v
```

## 6. Run one live conversation

```bash
python app.py
```

Test an unknown question, contextual memory, `clear history`, and `exit`.
