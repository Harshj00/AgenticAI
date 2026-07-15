Quick instructions to run the Streamlit UI

1. Install dependencies (prefer a virtualenv):

```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at http://localhost:8501 by default.

Notes:
- The backend agent uses the local LLM emulator in `llm.py`, so no external API keys are required.
- Use the sidebar "Clear Memory" button to wipe `memory.json`.
