from flask import Flask, request
from flask_cors import CORS, cross_origin

from flask_pymongo import PyMongo
from models.presentation import PresentationCollection
import socketio
import eventlet


UPLOAD_FOLDER = '/pdfs'

app = Flask('hackathon')
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sio = socketio.Server()

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


@sio.on('audio')
def handlechunk(sid, data):
    print(data)


if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)




