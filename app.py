from flask import Flask, request
from flask_pymongo import PyMongo
from models.presentation import PresentationCollection
import socketio
import eventlet


UPLOAD_FOLDER = '/pdfs'

app = Flask('hackathon')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sio = socketio.Server()

mongo = PyMongo(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.files['file'])
    presentation = PresentationCollection(mongo, app)
    presentation.add_presentation(request.files['file'])
    return 'file uploaded successfully'


@sio.on('audio')
def handlechunk(sid, data):
    print(data)


if __name__ == '__main__':
    # wrap Flask application with socketio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)