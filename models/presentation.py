import os
from bson.json_util import dumps
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId



class PresentationCollection:

    def __init__(self, mongo, app):
        self.mongo = mongo
        self.app = app

    def add_presentation(self, pdf_file):
        # save empty presentation without file
        result = self.mongo.db.presentations.insert_one({'originalFilename': secure_filename(pdf_file.filename)})
        # get id of empty record as filename
        filename = str(result.inserted_id)
        absolute_path = os.path.join(self.app.root_path + self.app.config['UPLOAD_FOLDER'], filename)
        # save file with id as filename
        pdf_file.save(absolute_path)
        # update record with path of file
        self.mongo.db.presentations.update_one({'_id': result.inserted_id}, {'$set': {'pdfPath': absolute_path}})
        return dumps(self.mongo.db.presentations.find_one({'_id': result.inserted_id}))

    def set_current_page(self, presentation_id, current_page):
        self.mongo.db.presentations.update_one({'_id': ObjectId(presentation_id)}, {'$set': {'currentPage': current_page}})
        return dumps(self.mongo.db.presentations.find_one({'_id': ObjectId(presentation_id)}))
