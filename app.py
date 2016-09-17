from flask import Flask, request
from flask_pymongo import PyMongo
from models.presentation import PresentationCollection

UPLOAD_FOLDER = '/pdfs'

app = Flask('hackathon')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = PyMongo(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.files['file'])
    presentation = PresentationCollection(mongo, app)
    presentation.add_presentation(request.files['file'])
    return 'file uploaded successfully'


