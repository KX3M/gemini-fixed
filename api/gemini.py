import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_response(message):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f'Tum ek friendly, caring, aur masti bhari ladki ho. Tum pyaar bhari aur cute baatein karti ho & tum "Hinglish" language mai baat Krna hindi mai nhi. User ka message: "{message}"'}
                    ]
                }
            ]
        }
        
        # Make the API request
        response = requests.post(url, json=payload)

        # Check if the response is successful
        if response.status_code != 200:
            return f"Error: {response.status_code}, {response.text}"

        data = response.json()

        # Check if 'candidates' exists in the response
        if "candidates" in data and data["candidates"]:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Invalid response from Gemini API"
    except Exception as e:
        return str(e)

@app.route("/gemini", methods=["GET"])
def chat():
    message = request.args.get("message")
    if not message:
        return jsonify({"error": "Message parameter is required"}), 400

    reply = generate_response(message)
    return jsonify({"reply": reply, "Owner": "@PythonBotz"})

@app.route("/gemini", methods=["POST"])
def chat_post():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Message is required"}), 400

    reply = generate_response(message)
    return jsonify({"reply": reply, "Owner": "@PythonBotz"})

if __name__ == "__main__":
    app.run(debug=True)