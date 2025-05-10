import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
from flask import render_template



# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_gemini():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    response = requests.post(
        GEMINI_API_URL,
        headers=headers,
        params={"key": API_KEY},
        json=payload
    )

    if response.status_code != 200:
        return jsonify({"error": "Gemini API error", "details": response.text}), 500

    result = response.json()
    try:
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"response": answer})
    except (KeyError, IndexError):
        return jsonify({"error": "Unexpected Gemini response format"}), 500

if __name__ == '__main__':
    app.run(debug=True)
