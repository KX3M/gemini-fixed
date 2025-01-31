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
                        {"text": f'Tu kaise ho? 😊 Tumhare message ka jawab dena hai! Main tumhe sweet aur thoda naughty tareeke se jawab dungi, hamesha Hinglish mein! 💖 Tumhare har question ka jawab dena mere liye bohot mazedaar hai! 😘 User ka message: "{message}"'}
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload)
        if response.status_code != 200:
            return f"Error: {response.status_code}, {response.text}"

        data = response.json()
        if "candidates" in data and data["candidates"]:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Invalid response from Gemini API"
    except Exception as e:
        return str(e)

# 🔹 GET request: Now uses /pythonbotz and ?msg=
@app.route("/pythonbotz", methods=["GET"])
def chat():
    message = request.args.get("msg")  # Changed from 'message' to 'msg'
    if not message:
        return jsonify({"error": "msg parameter is required"}), 400

    reply = generate_response(message)
    return jsonify({"reply": reply, "Owner": "@PythonBotz"})

# 🔹 POST request: Uses JSON body with "msg"
@app.route("/pythonbotz", methods=["POST"])
def chat_post():
    data = request.get_json()
    message = data.get("msg")  # Changed from 'message' to 'msg'
    if not message:
        return jsonify({"error": "msg is required"}), 400

    reply = generate_response(message)
    return jsonify({"reply": reply, "Owner": "@PythonBotz"})

if __name__ == "__main__":
    app.run(debug=True)