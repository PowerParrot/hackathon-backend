from flask import Flask, request
from flask_pymongo import PyMongo
from models.presentation import PresentationCollection


app = Flask('hackathon')
mongo = PyMongo(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    presentation = PresentationCollection(mongo, app)
    presentation.add_presentation(request.files[0])
    return 'file uploaded successfully'


