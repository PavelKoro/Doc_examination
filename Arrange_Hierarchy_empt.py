from Search_Head_empt import SearchHead
import re

class ArrangeHierarchy(SearchHead):
    def __init__(self, arr_data):
        SearchHead.__init__(self, arr_data)
        self.data = arr_data

    def check_hierarchy(self, text_id, end_text):
        """Определяет иерархию части текста."""
        text = self.data['texts'][text_id]['orig']

        stroka = text[0:end_text]
        rank = r'\d[.]|\d\s'
        """ Из текста берет: 
        - '\d[.]'
        --'цифра (\d) и точка, после цифр ([.])'

        - '|'
        -- 'или'
        
        - '\d\s'
        -- 'цифра (\d) и пробел, после цифры (\s)'

        Итог: ['1 ', '1.', '1.', '2.']"""

        result = re.findall(rank, stroka)
        
        rank_2 = r'\d[.]'
        """ Необходим, чтобы обнаружить фальшивую разметку, такие как 'ЦИФРА с ПРОБЕЛОМ' """
        """ ['1.', '1.', '2.'] """
        result_2 = re.findall(rank_2, stroka)

        itog = 0
        if len(result_2):
            itog = len(result)
        if itog == 0:
            itog = -1
        return itog

    def search_trash(self, text_id):
        text = self.data['texts'][text_id]['orig']
        chank_backet = r'[_]{3,}[/]\w{2,}'
        """
        - '[_]{3,}[/]\w{2,}'
        -- Взять только символ '_' c не менее трех повторений и взять символ '/' и взять слово, состоящее не менее двух букв
        Итог: ['________________/___________', '_______________/Лесков']
        """
        trash = re.findall(chank_backet, text)
        check_trash = 1
        if len(trash) != 0:
            check_trash = 0
        return check_trash

    def cerate_id_hierarchy(self, start_id, end_id):
        """Создает массив  пар с иерархей для текста и индексом текста, которому присваивали иерархию с 'start_id' до 'end_id' """
        """
        [[1, 4], [2, 5], [3, 6], [4, 7], [3, 8], [2, 9], [2, 10], [2, 11], [3, 12], [4, 15], [5, 16], [2, 17], [2, 18], [2, 19]]
        """
        count_before = self.check_hierarchy(start_id, 10)
        id_hierarchy = []
        check_text_id = 0

        for i in range(start_id, end_id+1):
            if self.check_label(i) != -1 and self.search_trash(i):
                count_after = self.check_hierarchy(i, 10)
                if count_after == -1:
                    check_text_id += 1
                    count_after = count_before + check_text_id
                else:
                    check_text_id = 0
                    count_before = count_after    
                id_hierarchy.append([count_after, i])
        return id_hierarchy

    def create_sequence_id(self, arr_id_hierarchy, i_id):
        """Создаем массив одного запроса с контекстом"""\
        """ 
        при arr_sequence(cerate_id_hierarchy(data, 4, 19), 4) -> [[1, 4], [2, 5], [3, 8]] или
        при arr_sequence(cerate_id_hierarchy(data, 4, 19), 5) -> [[1, 4], [2, 9]] и т.д.
        """
        arr_sequence = [arr_id_hierarchy[i_id]]
        check = i_id
        for i in range(i_id-1, -1, -1):
            if i != 0:
                if arr_id_hierarchy[check][0] > arr_id_hierarchy[i][0]:
                    check = i
                    arr_sequence.append(arr_id_hierarchy[i])
            else:
                arr_sequence.append(arr_id_hierarchy[i])

        new_arr_sequence = []
        for j in range(len(arr_sequence)-1, -1, -1):
            new_arr_sequence.append(arr_sequence[j])
        return new_arr_sequence

    def create_sequence_text(self, arr_sequence):
        """ Создает один запрос """
        """ '1. ПРЕДМЕТ ДОГОВОРА.\n1.1. В соответствии с условиями...\n1.1.2.  Осуществлять авторский надзор...Объекте.\n' """
        sequence_text = ''
        for i in range(len(arr_sequence)):
            sequence_text += self.data['texts'][arr_sequence[i][1]]['orig'] + '\n'
        return sequence_text

    def print_sequence_text(self, arr_sequence):
        """ 
        1. ПРЕДМЕТ ДОГОВОРА.
        1.1. В соответствии с условиями...работы):
        1.1.2.  Осуществлять авторский надзор...Объекте.
        """
        for i in range(len(arr_sequence)):
            print(self.data['texts'][arr_sequence[i][1]]['orig'])
        print('\n')

    def create_one_head_sequence_id(self, arr_id_hierarchy):
        """Создает массив всех id запросов с иерархией одной 'главы'"""
        """
        [
        [[1, 4], [2, 5], [3, 6], [4, 7]];
        [[1, 4], [2, 5], [3, 8]];
        [[1, 4], [2, 9]];
        [[1, 4], [2, 10]];
        [[1, 4], [2, 11], [3, 12], [4, 15], [5, 16]];
        [[1, 4], [2, 17]];
        [[1, 4], [2, 18]];
        [[1, 4], [2, 19]]
        ]
        """
        arr_one_head_sequence_id = []
        for i in range(len(arr_id_hierarchy)):
            if i != len(arr_id_hierarchy)-1:
                if arr_id_hierarchy[i][0] >= arr_id_hierarchy[i+1][0]:
                    arr_one_head_sequence_id.append(self.create_sequence_id(arr_id_hierarchy, i))
            else:
                arr_one_head_sequence_id.append(self.create_sequence_id(arr_id_hierarchy, i))
        return arr_one_head_sequence_id

    def create_one_head_sequence_texts(self, arr_one_head_sequence_id):
        """ Создает массив всех запросов текста одной 'главы' """
        arr_one_head_sequence_texts = []
        for i in range(len(arr_one_head_sequence_id)):
            text = self.create_sequence_text(arr_one_head_sequence_id[i])
            arr_one_head_sequence_texts.append(text)
        return arr_one_head_sequence_texts

    def print_one_head_sequence_texts(self, arr_one_head_sequence_id):
        for i in range(len(arr_one_head_sequence_id)):
            self.print_sequence_text(arr_one_head_sequence_id[i])

    def create_all_head_sequence_id(self, arr_id_head_plus):
        """ Создает массив всех id запросов с иерархией всех 'глав' документа """
        arr_all_head_sequence_id = []
        for i in range(len(arr_id_head_plus)):
            arr_id_hierarchy = self.cerate_id_hierarchy(arr_id_head_plus[i][0], arr_id_head_plus[i][1])
            arr_one_head_sequence_id = self.create_one_head_sequence_id(arr_id_hierarchy)
            arr_all_head_sequence_id.append(arr_one_head_sequence_id)
        return arr_all_head_sequence_id

    def create_all_head_sequence_texts(self, arr_all_head_sequence_id):
        """ Создает массив всех запросов текста всех 'глав' документа """
        arr_all_head_sequence_texts = []
        for i in range(len(arr_all_head_sequence_id)):
            arr_one_head_sequence_texts = self.create_one_head_sequence_texts(arr_all_head_sequence_id[i])
            arr_all_head_sequence_texts.append(arr_one_head_sequence_texts)
        return arr_all_head_sequence_texts

    def print_all_head_sequence_texts(self, arr_all_head_sequence_id):
        for i in range(len(arr_all_head_sequence_id)):
            print(f"\n\n################# Глава {i} #################\n")
            self.print_one_head_sequence_texts(arr_all_head_sequence_id[i])
        
    def process_create_queries(self):
        """Обрабатывает JSON данные и выводит результаты."""
        id_head = self.create_id_head()
        id_head_plus = self.create_id_head_plus(id_head)
        all_head_sequence_id = self.create_all_head_sequence_id(id_head_plus)
        all_head_sequence_texts = self.create_all_head_sequence_texts(all_head_sequence_id)
        return all_head_sequence_texts

    def print_process_create_queries(self):
        id_head = self.create_id_head()
        id_head_plus = self.create_id_head_plus(id_head)
        all_head_sequence_id = self.create_all_head_sequence_id(id_head_plus)
        self.print_all_head_sequence_texts(all_head_sequence_id)