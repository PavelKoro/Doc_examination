from docling.document_converter import DocumentConverter
import os
import json

class PdfJsonConverter:
    def __init__(self, db, doc_name, source_pdf):
        self.db = db
        self.doc_name = doc_name
        self.source = source_pdf
        if not db.check_pdf_json_exists(self.doc_name, self.source):
            json = self.convert_pdf_to_document()
            db.push_PDF_JSON_table(self.doc_name, self.source, json)
        else:
            print(f"[INFO]: Inserted 'PDF_JSON' unsuccessful: in '{self.doc_name}' already exists '{self.source}'")


    def convert_pdf_to_document(self):
        """Конвертирует PDF-файл в объект документа."""
        converter = DocumentConverter()
        result = converter.convert(self.source)

        """Экспортирует объект документа в словарь."""
        dict_data = result.document.export_to_dict()

        """Преобразует словарь в JSON строку."""
        json_data = json.dumps(dict_data, ensure_ascii=False, indent=4)
        print(f'Готово: {self.source}')
        return json_data