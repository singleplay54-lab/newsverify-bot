import os
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/")
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        print("Incoming update:", data)

        if "message" not in data:
            return "ok", 200

        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if not text:
            return "ok", 200

        reply = fact_check(text)

        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": reply
            },
            timeout=10
        )

        return "ok", 200

    except Exception as e:
        print("Webhook error:", e)
        return "ok", 200   # 🔥 VERY IMPORTANT

def fact_check(text):
    return f"🧪 Fact-check received:\n\n{text}\n\n( AI response coming soon 🚀 )"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

