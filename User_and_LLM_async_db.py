from PDF_JSON_Converter_empt import PdfJsonConverter
from Singleton_postg_empt import Singleton_postg
from expertise import get_gpt_response
from Requests_empt import Requests

import json_repair
import asyncio
import time 

def registration(db, email, password):
    user_id = db.get_Users_table(email, password)
    if len(user_id) == 0:
        user_id = db.push_Users_table(email, password) ## Регистрируем пользователя
        print("Зарегистрировали пользователя")
    else:
        print(f"Пользователь Users={user_id[0]} -> email={email}: {password} уже зарегистрирован.")
    return user_id[0]

def get_database_content(db, doc_name, user_id):
    setting_llm = db.get_setting_llm_by_id(user_id, 1)
    prompt = setting_llm['prompt']
    
    key_provisions_user = db.get_questions_comments_table(doc_name)
    questions = key_provisions_user['questions']
    remarks = key_provisions_user['comments']
    return prompt, questions, remarks

async def process_document(db, doc_name, file_name, prompt, questions, remarks):
    resultat_doc = Requests(db, doc_name, file_name, prompt, questions, remarks)
    user_requests = resultat_doc.create_user_requests()

    # Установите лимит на количество одновременных соединений
    semaphore_limit = 1000
    semaphore = asyncio.Semaphore(semaphore_limit)
    tasks = []
    for i in range(len(user_requests)):
        for j in range(len(user_requests[i])):
            for k in range(len(user_requests[i][j])):
                # Создаем coroutine для каждого запроса
                task = get_gpt_response(user_requests[i][j][k], semaphore)
                # Добавляем созданную coroutine в список задач
                tasks.append(task)
    # Выполняем все задачи параллельно и ждем их завершения
    arr_answeres = await asyncio.gather(*tasks)
    return arr_answeres

def analyze_responses(answeres, questions):
    arr_section_item = []
    arr_item = []
    count = len(answeres) / len(questions)
    print(f"count {count}")
    print(f"answeres {len(answeres)}")
    k = 1
    for i in range(len(answeres)):
        data = json_repair.loads(answeres[i])    
        if(i == (k*count - 1)):
            if data['Check_Question'] == 'True':
                arr_item.append(data['Section_item'])
            arr_section_item.append(arr_item)
            arr_item = []
            k += 1
        if data['Check_Question'] == 'True':
            arr_item.append(data['Section_item'])
    return arr_section_item

def output(answeres, questions):
    arr_section_item = analyze_responses(answeres, questions)
    for i in range(len(arr_section_item)):
        print(f"\n\n##################### {questions[i]} #####################")
        for j in range(len(arr_section_item[i])):
            print(arr_section_item[i][j], end='; ')

def main():
    email = 'p.korol2003@gmail.com'
    password = '123'
    doc_name = 'Проектирование'
    file_name = 'PDF/2.pdf'

    db = Singleton_postg()

    user_id = registration(db, email, password)
    pdf_converter = PdfJsonConverter(db, doc_name, file_name)
    prompt, questions, remarks = get_database_content(db, doc_name, user_id)
    print("Собрали все необходимые данные: prompt, questions, remarks")
    answers = asyncio.run(process_document(db, doc_name, file_name, prompt, questions, remarks))
    output(answers, questions)

    db.close_connection()

start = time.time()
main()
finish = time.time()
print(f"\n\nWorking time = {round(finish-start ,2)} seconds")