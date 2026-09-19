from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os

from chatbot_configuration import CHATBOT_NAME, SYSTEM_PROMPT

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Please add it to the .env file."
    )

# Create Gemini client
client = genai.Client(api_key=API_KEY)


@app.route("/")
def home():
    return render_template(
        "index.html",
        chatbot_name=CHATBOT_NAME
    )


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please enter a travel-related question."
            })

        prompt = f"""
{SYSTEM_PROMPT}

User Question:
{user_message}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("Error:", e)

        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
