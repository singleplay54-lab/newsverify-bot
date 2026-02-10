import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "no data"}), 200

    if "message" not in data:
        return jsonify({"status": "ignored"}), 200

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    if not text:
        return jsonify({"status": "no text"}), 200

    reply = f"🧠 Fact-check received:\n\n{text}"

    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": reply
        },
        timeout=10
    )

    return jsonify({"status": "ok"}), 200


