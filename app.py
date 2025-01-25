from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from persona_chatbot import PersonaChatbot
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

# Global chatbot instance
chatbot = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        file.save('human_chat.txt')
        global chatbot
        chatbot = PersonaChatbot()
        return jsonify({
            'success': True,
            'persona': chatbot.persona
        })

@socketio.on('message')
def handle_message(data):
    if chatbot is None:
        emit('response', {'error': 'Please upload chat data first'})
        return
    
    try:
        response = chatbot.generate_response(data['message'])
        context = chatbot.get_last_context()  # Add this method to PersonaChatbot class
        emit('response', {
            'message': response,
            'context': context
        })
    except Exception as e:
        emit('response', {'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)