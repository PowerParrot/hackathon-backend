import os
from werkzeug.utils import secure_filename


class PresentationCollection:

    def __init__(self, mongo, app):
        self.mongo = mongo
        self.app = app

    def add_presentation(self, pdf_file):
        # save empty presentation without file
        result = self.mongo.db.presentations.insert_one({'originalFilename': secure_filename(pdf_file.filename)})

        # get id of empty record as filename
        filename = result.inserted_id

        # save file with id as filename
        pdf_file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))

        # update record with path of file
        self.mongo.db.presentation.update_one({'_id': filename}, {'$set': {'pdfPath': pdf_file.name}})
