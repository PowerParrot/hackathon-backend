from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask('hackathon')
mongo = PyMongo(app)

UPLOAD_FOLDER = '/pdfs'

