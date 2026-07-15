import sys
from pathlib import Path

from flask import Flask, jsonify, request

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from agent import Agent

app = Flask(__name__)
agent = Agent()


@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Please enter a message."}), 400

    try:
        reply = agent.run(message)
        return jsonify({"reply": reply})
    except Exception as exc:
        return jsonify({"reply": f"Error: {exc}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
