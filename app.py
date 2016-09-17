from flask import Flask, request, url_for
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
import json

from models.presentation import PresentationCollection


UPLOAD_FOLDER = '/static/pdfs'

app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=['Accept-Ranges'])

# socket.io
socketio = SocketIO(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = PyMongo(app)
presentation = PresentationCollection(mongo, app)


@app.route('/upload', methods=['POST'])
def upload_file():
    created_presentation = presentation.add_presentation(request.files['file'])
    return created_presentation


@app.route('/changePage', methods=['PUT'])
def change_page():
    updated_presentation = presentation.set_current_page(request.args.get('presentation_id'), request.args.get('current_page'))
    return updated_presentation


@app.route('/getDocumentPath', methods=['GET'])
def get_file_url():
    object_id = request.args.get('presentation_id')
    json_object = {'url': url_for('static', filename='pdfs/' + object_id)}
    return json.dumps(json_object)

if __name__ == '__main__':
    socketio.run(app)
