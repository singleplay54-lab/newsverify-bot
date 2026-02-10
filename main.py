from flask import Flask, request
import requests
import google.generativeai as genai
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"]["text"]

    prompt = f"""
    Check this news or claim for Indian users:

    "{user_text}"

    Reply in simple Hinglish.
    Say if it is Likely True, Fake, Misleading, or Unverified.
    Give short reason.
    Add disclaimer that this is not final judgement.
    """

    response = model.generate_content(prompt)
    send_message(chat_id, response.text)

    return "ok"

@app.route("/")
def home():
    return "Bot is running"
