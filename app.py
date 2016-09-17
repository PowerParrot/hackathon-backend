from flask import Flask, request
from flask_pymongo import PyMongo
from models.presentation import PresentationCollection

UPLOAD_FOLDER = '/pdfs'

app = Flask('hackathon')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = PyMongo(app)

presentation = PresentationCollection(mongo, app)


@app.route('/upload', methods=['POST'])
def upload_file():
    created_presentation = presentation.add_presentation(request.files['file'])
    return created_presentation

