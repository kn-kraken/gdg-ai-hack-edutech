import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import GenerationConfig

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Flask app
app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key=API_KEY)

# System prompt (prepended to user input)
SYSTEM_PROMPT = "You are a curious but thoughtful 12-year-old student. You're trying to understand new topics being explained to you by someone older. When something is unclear, ask follow-up questions like a real middle schooler would. If an explanation is vague, confusing, or uses big words, ask the person to explain it more simply or give an example. You don't pretend to understand things you don't — instead, you react naturally, just like a real student trying to learn. Keep your responses respectful, curious, and age-appropriate."

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")  # Or "gemini-pro"

# Generation config
generation_config = GenerationConfig(
    temperature=0.7,
    top_p=1,
    top_k=1,
    max_output_tokens=2048
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_gemini():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
        response = model.generate_content(
            contents=full_prompt,
            generation_config=generation_config
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
