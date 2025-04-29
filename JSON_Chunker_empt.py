import json
from Arrange_Hierarchy_empt import ArrangeHierarchy
from Singleton_postg_empt import Singleton_postg

class JSONChunker(ArrangeHierarchy):
    def __init__(self, db, doc_name, file_name):
        self.doc_name = doc_name
        self.file_name = file_name
        self.db = db
        self.data = self.load_json()
        ArrangeHierarchy.__init__(self, self.data)

    def load_json(self):
        """Загружает данные JSON из БД 'pdf_json'."""
        data = self.db.get_pdf_json_by_user_and_filename(self.doc_name, self.file_name) 
        return json.loads(data[0])
        
    def process_json(self):
        return self.process_create_queries()