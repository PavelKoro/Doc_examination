import psycopg2

class Singleton_postg:
    isinstance = None
    _connection = None

    _Users_table = False
    _Setting_LLM_table = False
    _Doc_folder_table = False
    _questions_comments_table = False
    _PDF_JSON_table = False

    def __new__(cls):
        if Singleton_postg.isinstance is None:
            Singleton_postg.isinstance = super(Singleton_postg, cls).__new__(cls)
            cls._connection = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="qwerty",
                host="localhost",
                port="5432"
            )
        return Singleton_postg.isinstance
    
    def get_connection(self):
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self.isinstance = None

    def drop_table(self, table_name: str):
        cursor = self._connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
        self._connection.commit()
        k = self.false_table(table_name)
        print(f"[INFO]: isinstance = {self.isinstance} -> Table '{table_name}' dropped successfully. -> '{table_name}' = {k}")
        cursor.close()
        
    def false_table(self, table_name: str):
        chek = True
        if table_name == 'Users':
            self._Users_table = False
            chek = False
        elif table_name == 'Setting_LLM':
            self._Setting_LLM_table = False
            chek = False
        elif table_name == 'Doc_folder':
            self._Doc_folder_table = False
            chek = False
        elif table_name == 'questions_comments':
            self._questions_comments_table = False
            chek = False
        elif table_name == 'PDF_JSON':
            chek = False
        return chek

################# Users #################
    def create_Users_table(self):
        if self._Users_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'Users' exists.")
            return
        
        cursor = self._connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')
        self._connection.commit()
        self._Users_table = True
        print(f"[INFO]: isinstance = {self.isinstance} -> Create table 'Users' successfully.")
        cursor.close()
    
    def push_Users_table(self, email, password):
        if not self._Users_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'Users' does not exists.")
            self.create_Users_table()
        
        cursor = self._connection.cursor()
        cursor.execute('''
        INSERT INTO Users (email, password)
        VALUES (%s, %s)
        ''', (email, password))
        arr_user_id = self.get_Users_table(email, password)

        self._connection.commit()
        print(f"[INFO]: Inserted Users={arr_user_id[0]} -> email={email}: {password} successfully.")
        cursor.close()
        return arr_user_id
    
    def get_Users_table(self, email, password):
        cursor = self._connection.cursor()
        cursor.execute('SELECT user_id FROM Users WHERE email = %s AND password = %s', (email, password))
        rows = cursor.fetchall()
        
        arr_user_id = [row[0] for row in rows]
        cursor.close()
        return arr_user_id

################# Setting_LLM #################
    def create_Setting_LLM_table(self):
        if self._Setting_LLM_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'Setting_LLM' exists.")
            return 1
        
        cursor = self._connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Setting_LLM (
            setting_id SERIAL PRIMARY KEY,
            user_id INTEGER,
            prompt TEXT NOT NULL,
            model TEXT NOT NULL,
            top_p REAL NOT NULL,
            temperature REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users (user_id)
        )
        ''')
        self._connection.commit()
        self._Setting_LLM_table = True
        print(f"[INFO]: isinstance = {self.isinstance} -> Create table 'Setting_LLM' successfully.")
        cursor.close()

    def push_Setting_LLM_table(self, user_id, prompt, model, top_p, temperature):
        if not self._Setting_LLM_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'Setting_LLM' does not exists.")
            self.create_Setting_LLM_table()
    
        cursor = self._connection.cursor()
        cursor.execute('''
        INSERT INTO Setting_LLM (user_id, prompt, model, top_p, temperature)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING setting_id
        ''', (user_id, prompt, model, top_p, temperature))
        setting_id = cursor.fetchone()[0]
        self._connection.commit()
        print(f"[INFO]: Inserted 'Setting_LLM' successfully: user_id = {user_id} -> setting_id={setting_id}")
        cursor.close()
        return setting_id

    def get_setting_llm_by_user(self, user_id):
        cursor = self._connection.cursor()
        cursor.execute('SELECT setting_id, prompt, model, top_p, temperature FROM Setting_LLM WHERE user_id = %s', (user_id,))
        rows = cursor.fetchall()
        
        arr_setting_id = [row[0] for row in rows]
        prompts = [row[1] for row in rows]
        models = [row[2] for row in rows]
        top_ps = [row[3] for row in rows]
        temperatures = [row[4] for row in rows]
        
        cursor.close()
        return {
            'setting_id': arr_setting_id,
            'prompts': prompts,
            'models': models,
            'top_ps': top_ps,
            'temperatures': temperatures
        }
    
    def get_setting_llm_by_id(self, user_id, setting_id):
        cursor = self._connection.cursor()
        cursor.execute('''
        SELECT prompt, model, top_p, temperature
        FROM Setting_LLM
        WHERE user_id = %s AND setting_id = %s
        ''', (user_id, setting_id))
        
        # Получаем одну запись, если она существует
        row = cursor.fetchone()
        if row:
            return {
                "prompt": row[0],
                "model": row[1],
                "top_p": row[2],
                "temperature": row[3]
            }
        else:
            print(f"No setting found for user_id={user_id} and setting_id={setting_id}.")
            cursor.close()
            return None

################# Doc_folder ################# 
    def create_Doc_folder_table(self):
        if self._Doc_folder_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'Doc_folder' exists.")
            return
        
        cursor = self._connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doc_folder (
            user_id INTEGER,
            doc_name TEXT NOT NULL UNIQUE,
            FOREIGN KEY (user_id) REFERENCES Users (user_id)
        )
        ''')
        self._connection.commit()
        self._Doc_folder_table = True
        print(f"[INFO]: isinstance = {self.isinstance} -> Create table 'Doc_folder' successfully.")
        cursor.close()

    def push_Doc_folder_table(self, user_id, doc_name):
        if not self._Doc_folder_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'Doc_folder' does not exists.")
            self.create_Doc_folder_table()
        
        cursor = self._connection.cursor()
        cursor.execute('''
        INSERT INTO Doc_folder (user_id, doc_name)
        VALUES (%s, %s)
        ''', (user_id, doc_name))
        self._connection.commit()
        print(f"[INFO]: Inserted 'Doc_folder' successfully: user_id = {user_id} -> doc_name = {doc_name}")
        cursor.close()

    def get_Doc_folder_table(self, user_id):
        cursor = self._connection.cursor()
        cursor.execute('SELECT doc_name FROM Doc_folder WHERE user_id = %s', (user_id,))
        rows = cursor.fetchall()
        arr_doc_name = [row[0] for row in rows]
        cursor.close()
        return arr_doc_name
    
    def check_doc_name_exists(self, user_id, doc_name):
        cursor = self._connection.cursor()
        cursor.execute('''
        SELECT EXISTS(
            SELECT 1
            FROM Doc_folder
            WHERE user_id = %s AND doc_name = %s
        )
        ''', (user_id, doc_name))

        exists = cursor.fetchone()[0]
        cursor.close()
        return int(exists)



################# questions_comments #################
    def create_questions_comments_table(self):
        if self._questions_comments_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'questions_comments' exists.")
            return 1
        
        cursor = self._connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions_comments (
            doc_name TEXT NOT NULL,
            questions TEXT NOT NULL,
            comments TEXT NOT NULL,
            FOREIGN KEY (doc_name) REFERENCES Doc_folder (doc_name)
        )
        ''')
        self._connection.commit()
        self._questions_comments_table = True
        print(f"[INFO]: isinstance = {self.isinstance} -> Create table 'questions_comments' successfully.")
        cursor.close()
    
    def push_questions_comments_table(self, doc_name, question, comment, check = 1):
        if not self._questions_comments_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'questions_comments' does not exists.")
            self.create_questions_comments_table()
        
        cursor = self._connection.cursor()
        cursor.execute('''
        INSERT INTO questions_comments (doc_name, questions, comments)
        VALUES (%s, %s, %s)
        ''', (doc_name, question, comment))
        self._connection.commit()
        if check:
            print(f"[INFO]: Inserted 'questions_comments' successfully: {doc_name} -> \n\t{question}\n\t{comment}")
        cursor.close()

    def all_push_questions_comments_table(self, doc_name, arr_question, arr_comment):
        if not self._questions_comments_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'questions_comments' does not exists.")
            self.create_questions_comments_table()
        for i in range(len(arr_question)):
            self.push_questions_comments_table(doc_name, arr_question[i], arr_comment[i], 0)
        print(f"[INFO]: Inserted 'questions_comments' successfully: {doc_name} -> questions and comments")

    def get_questions_comments_table(self, doc_name):
        cursor = self._connection.cursor()
        cursor.execute('SELECT questions, comments FROM questions_comments WHERE doc_name = %s', (doc_name,))
        rows = cursor.fetchall()
        questions = [row[0] for row in rows]
        comments = [row[1] for row in rows]
        cursor.close()
        return {'questions': questions, 'comments': comments}

################# PDF_JSON #################
    def create_PDF_JSON_table(self):
        if self._PDF_JSON_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'PDF_JSON' exists.")
            return
        
        cursor = self._connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS PDF_JSON (
            doc_name TEXT NOT NULL,
            file_name TEXT NOT NULL,
            json TEXT NOT NULL,
            FOREIGN KEY (doc_name) REFERENCES Doc_folder (doc_name)
        )
        ''')
        self._connection.commit()
        self._PDF_JSON_table = True
        print(f"[INFO]: isinstance = {self.isinstance} -> Create table 'PDF_JSON' successfully.")
        cursor.close()

    def check_pdf_json_exists(self, doc_name, file_name):
        cursor = self._connection.cursor()
        cursor.execute('''
        SELECT EXISTS(
            SELECT 1
            FROM PDF_JSON
            WHERE doc_name = %s AND file_name = %s
        )
        ''', (doc_name, file_name))

        exists = cursor.fetchone()[0]
        cursor.close()
        return int(exists)

    def push_PDF_JSON_table(self, doc_name, file_name, json):
        if not self._PDF_JSON_table:
            print(f"[INFO]: isinstance = {self.isinstance} -> The table 'PDF_JSON' does not exists.")
            self.create_PDF_JSON_table()
        
        if self.check_pdf_json_exists(doc_name, file_name):
            print(f"[INFO]: Inserted 'PDF_JSON' unsuccessful: in '{doc_name}' already exists '{file_name}'")
            return 0

        cursor = self._connection.cursor()
        cursor.execute('''
        INSERT INTO PDF_JSON (doc_name, file_name, json)
        VALUES (%s, %s, %s)
        ''', (doc_name, file_name, json))
        self._connection.commit()
        print(f"[INFO]: Inserted 'PDF_JSON' successfully: {doc_name} -> {file_name}")
        cursor.close()
        return 1
    
    def get_pdf_json_by_user_and_filename(self, doc_name, file_name):
        cursor = self._connection.cursor()
        cursor.execute('SELECT json FROM PDF_JSON WHERE doc_name = %s AND file_name = %s', (doc_name, file_name))
        rows = cursor.fetchall()
        json_data = [row[0] for row in rows]
        cursor.close()
        return json_data