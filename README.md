# Agentic AI Frontend

This project now includes a simple browser-based frontend for the local agent.

## Run locally

```bash
pip install -r requirements.txt
python api/chat.py
```

For the frontend files, serve the project root with a simple static server:

```bash
python -m http.server 8000
```

Then open:

- http://127.0.0.1:8000 for the frontend
- http://127.0.0.1:5000/api/chat for the API

## Deploy on GitHub + Vercel

1. Create a GitHub repository and push this project.
2. Import the repository in Vercel.
3. Deploy.

The deployment config is already included in [vercel.json](vercel.json).
