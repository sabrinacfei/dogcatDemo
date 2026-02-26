from flask import Flask, render_template, request, jsonify, session
import os
from google import genai

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"].strip())
MODEL_ID = "gemini-2.5-flash"

def generate_response(pet, text, user_id):
    if "chat_history" not in session:
        session["chat_history"] = {}

    if user_id not in session["chat_history"]:
        session["chat_history"][user_id] = []  

    session["chat_history"][user_id].append(f"主人：{text}")

    chat_context = "\n".join(session["chat_history"][user_id])
    prompt = f"你是一隻{'快樂的小狗狗名字叫麻吉' if pet == 'dog' else '驕傲的貓咪名字叫米菲'}，並且會依照設定的個性簡單回答主人的問題。\n以下是與主人的對話：\n{chat_context}\nAI 回應："

    resp = client.models.generate_content(model=MODEL_ID, contents=prompt)
    response = (resp.text or "").strip()

    session["chat_history"][user_id].append(f"AI：{response}")

    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    pet = data.get('pet', '')
    user_id = request.remote_addr 

    response = generate_response(pet, text, user_id)

    return jsonify({'response': response, 'pet': pet})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="0.0.0.0", port=port)
