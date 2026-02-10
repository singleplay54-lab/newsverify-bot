import os
from flask import Flask, request
import google.generativeai as genai

app = Flask(__name__)

# Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def home():
    return "NewsVerify Bot is running ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = data["message"]["text"]

    prompt = f"""
    Fact check the following news claim.
    Reply in simple Hindi + English mix.
    Also suggest trusted sources.

    Claim: {message}
    """

    response = model.generate_content(prompt)
    reply = response.text

    chat_id = data["message"]["chat"]["id"]
    token = os.environ.get("BOT_TOKEN")

    import requests
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )

    return "ok"

