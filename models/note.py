from bson.json_util import dumps


class NotesCollection:

    def __init__(self, mongo):
        self.mongo = mongo

    def add_note(self, note_json):
        self.mongo.db.notes.insert_one(note_json)

    def get_notes_for_presentation(self, presentation_id):
        return dumps(self.mongo.db.notes.find({"presentation_id": presentation_id}))