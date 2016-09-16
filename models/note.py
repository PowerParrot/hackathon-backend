class NotesCollection:

    def __init__(self, mongo):
        self.mongo = mongo

    def add_note(self, note_json):
        self.mongo.db.notes.insert_one(note_json)

