from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from flask_pymongo import PyMongo

from models.presentation import PresentationCollection

from services.speech_to_text import SpeechToText

UPLOAD_FOLDER = '/pdfs'

app = Flask(__name__)
CORS(app)

# socket.io
socketio = SocketIO(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = PyMongo(app)
presentation = PresentationCollection(mongo, app)

google_service = None

@app.route('/upload', methods=['POST'])
def upload_file():
    created_presentation = presentation.add_presentation(request.files['file'])
    return created_presentation


@app.route('/changePage', methods=['PUT'])
def change_page():
    updated_presentation = presentation.set_current_page(request.args.get('presentation_id'), request.args.get('current_page'))
    return updated_presentation


@socketio.on('audio')
def handlechunk(data):
    socketio.emit('message', {'data': 'fudejasse'})
    google_service.handle_chunk(data)


@socketio.on('init')
def handleinit(message):
    google_service = SpeechToText()

if __name__ == '__main__':
    socketio.run(app)
