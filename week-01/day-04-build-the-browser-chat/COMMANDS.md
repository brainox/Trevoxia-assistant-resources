# Day 4 Commands

These commands appear in the same order as the Week 1, Day 4 tutorial.

## 1. Open the project and verify the Day 3 baseline

```bash
cd trexovia-assistant
git pull
source .venv/bin/activate
python --version
python -m pip --version
python -m pip install -r requirements.txt
python -m compileall -q app.py llm.py memory.py tests
python -m unittest discover -s tests -v
```

> Windows PowerShell: `.venv\Scripts\Activate.ps1`

The Day 3 baseline should report nine passing tests.

## 2. Create the browser and workflow test files

```bash
touch ui.py tests/test_chat.py
```

## 3. Install the browser-interface dependency

```bash
python -m pip install streamlit==1.50.0
```

Add the same pinned version to `requirements.txt`.

## 4. Compile and run all offline tests

```bash
python -m compileall -q app.py llm.py memory.py ui.py tests
python -m unittest discover -s tests -v
```

Expected result: `Ran 12 tests` followed by `OK`.

## 5. Start the browser chat

```bash
python -m streamlit run ui.py
```

Test a normal message, a follow-up that uses memory, the message counters, the clear-history button, and persistence after restarting Streamlit.
