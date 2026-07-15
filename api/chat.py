import sys
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from agent import Agent

app = Flask(__name__)
agent = Agent()


# Serve frontend static files (index.html, app.js, styles.css, etc.)
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(str(ROOT), "index.html")


@app.route("/<path:path>", methods=["GET"])
def static_proxy(path):
    # avoid exposing python source or backend endpoints through the static proxy
    if path.startswith("api/") or path.endswith(".py"):
        return ("Not Found", 404)
    return send_from_directory(str(ROOT), path)


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
