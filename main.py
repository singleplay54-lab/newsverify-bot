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

    # 🔥 Gemini API call (INSIDE webhook)
    gemini_url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-pro:generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [{
            "parts": [{
                "text": f"""
You are a fact-checking AI.
Classify the claim as True / False / Misleading.
Explain briefly in simple language.

Claim: {text}
"""
            }]
        }]
    }

    try:
        r = requests.post(gemini_url, json=payload, timeout=20)
        gemini_reply = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        gemini_reply = "⚠️ AI error. Please try again."

    # 📤 Send Gemini reply to Telegram
    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": gemini_reply
        }
    )

    return jsonify({"status": "ok"}), 200


