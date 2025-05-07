from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Păstrează istoricul conversațiilor
chat_history = []

# Încarcă istoricul din fișier (dacă există)
HISTORY_FILE = 'chat_history.json'
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r') as f:
        chat_history = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@socketio.on('send_message')
def handle_message(data):
    # Simulează răspunsul Llama (aici poți integra cu API-ul Llama)
    user_message = data['message']
    bot_response = f"Răspuns Llama la: {user_message}"
    
    # Adaugă mesajele la istoric
    chat_history.append({'user': user_message, 'bot': bot_response})
    
    # Salvează istoricul în fișier
    with open(HISTORY_FILE, 'w') as f:
        json.dump(chat_history, f)
    
    # Trimite răspunsul înapoi la client
    emit('receive_message', {'user': user_message, 'bot': bot_response}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)