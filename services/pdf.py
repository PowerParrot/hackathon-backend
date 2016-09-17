from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
import os
import json
from reportlab.lib.pagesizes import A4, legal, landscape, A5, A3, portrait
from reportlab.pdfgen.canvas import Canvas
from models.note import NotesCollection


class PdfExporter:

    def __init__(self, presentation_id, mongo, app):
        self.presentation_id = presentation_id
        self.notes_collection = NotesCollection(mongo)
        self.app = app
        self.presentation = os.path.join(self.app.root_path + self.app.config['UPLOAD_FOLDER'], presentation_id)

    def generate(self):
        final_file = PdfFileWriter()

        presi = PdfFileReader(file(self.presentation, 'rb'))
        numpages = presi.getNumPages()

        for i in range(0, numpages):
            final_file.addPage(presi.getPage(i))
            final_file.addPage(self.create_notes_page(i+1).getPage(0))

        outputStream = file(self.presentation+'_report', "wb")
        final_file.write(outputStream)
        outputStream.close()

    def create_notes_page(self, page_number):
        packet = StringIO.StringIO()

        canvas = Canvas(packet, pagesize=landscape(A4))
        notes = json.loads(self.notes_collection.get_notes_for_presentation(self.presentation_id))
        line = 550
        for note in notes:
            if int(note['current_page']) == page_number:
                canvas.drawString(10, line, note['speech'])
                line -= 15
        canvas.showPage()
        canvas.save()
        packet.seek(0)
        notes_pdf = PdfFileReader(packet)
        return notes_pdf