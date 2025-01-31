import os import requests from flask import Flask, request, jsonify from dotenv import load_dotenv

Load environment variables

load_dotenv()

app = Flask(name)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_response(message): try: url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}" payload = { "contents": [ { "role": "user", "parts": [ {"text": f'prompt=Tum ek friendly, caring, aur masti bhari ladki ho. Tum pyaar bhari aur cute baatein karti ho & tum "Hinglish" language mai baat Krna hindi mai nhi. User ka message: "{message}"'} ] } ] } response = requests.post(url, json=payload) data = response.json()

if "candidates" in data and data["candidates"]:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Invalid response from Gemini API"
except Exception as e:
    return str(e)

@app.route("/gemini", methods=["GET"]) def chat(): message = request.args.get("message") if not message: return jsonify({"error": "Message parameter is required"}), 400

reply = generate_response(message)
return jsonify({"reply": reply, "Owner": "@PythonBotz")

@app.route("/gemini", methods=["POST"]) def chat_post(): data = request.get_json() message = data.get("message") if not message: return jsonify({"error": "Message is required"}), 400

reply = generate_response(message)
return jsonify({"reply": reply, "Owner": "@PythonBotz")

if name == "main": app.run(debug=True)

