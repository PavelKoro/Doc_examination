from JSON_Chunker_empt import JSONChunker

class Requests(JSONChunker):
    def __init__(self, db, doc_name, file_name, prompt, arr_questions, arr_remarks):
        JSONChunker.__init__(self, db, doc_name, file_name)
        self.text_chunks = self.process_json()

        self.prompt = prompt
        self.questions = arr_questions
        self.remarks = arr_remarks

    def create_one_user_question_one_head(self, text_question, arr_text_chunks_one_head, text_remarks):
        arr_stroka_one_head = []
        for i in range(len(arr_text_chunks_one_head)):
            stroka = 'Инструкция: ' + self.prompt + '\n\n' + 'Вопрос: ' + text_question + '\n\n' + 'Текст документа: ' + arr_text_chunks_one_head[i] + '\n' + 'Комментарий: ' + text_remarks + '\n\n' + 'Инструкция: ' + self.prompt
            arr_stroka_one_head.append(stroka)
        return arr_stroka_one_head
    
    def print_one_user_question_one_head(self, arr_stroka_one_head, count):
        k = count
        for i in range(len(arr_stroka_one_head)):
            print(f"---> Запрос: {k}")
            print(arr_stroka_one_head[i])
            print("\n")
            k += 1
    
    def create_one_user_question_all_doc(self, text_question, text_remarks):
        arr_stroka_all_head = []
        for i in range(len(self.text_chunks)):
            stroka_one_head = self.create_one_user_question_one_head(text_question, self.text_chunks[i], text_remarks)
            arr_stroka_all_head.append(stroka_one_head)
        return arr_stroka_all_head
    
    def print_one_user_question_all_doc(self, arr_stroka_all_head, count):
        k = count
        for i in range(len(arr_stroka_all_head)):
            print(f"--> Глава: {i}")
            self.print_one_user_question_one_head(arr_stroka_all_head[i], k)
            k += len(arr_stroka_all_head[i])
    
    def create_user_requests(self):
        arr_user_requests = []
        for i in range(len(self.questions)):
            one_user_question_all_doc = self.create_one_user_question_all_doc(self.questions[i], self.remarks[i])
            arr_user_requests.append(one_user_question_all_doc)
        return arr_user_requests
    
    def sum_count(self, arr_stroka_all_head):
        k = 0
        for i in range(len(arr_stroka_all_head)):
            k += len(arr_stroka_all_head[i])
        return k

    def print_user_requests(self, arr_user_requests):
        count = 1
        for i in range(len(arr_user_requests)):
            print(f"-> Загаловок: {i}")
            self.print_one_user_question_all_doc(arr_user_requests[i], count)
            count += self.sum_count(arr_user_requests[i])