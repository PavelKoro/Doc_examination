import re

class SearchHead:
    def __init__(self, arr_data):
        self.data = arr_data

    def check_headings(self, text_id):
        """Проверяет, является ли текст заголовком."""
        text = self.data['texts'][text_id]['orig']

        pattern_head = r'\d+\.\s+|\d+\s+|\d+\.'
        """ Из текста берет: 
        - '\d+\.\s+'
        --'посл-ть цифр (\d+) и точку, после цифр (\.) и посл-ть пробелов, после точки (\s+)'

        - '|'
        -- 'или'
        
        - '\d+\s+'
        -- 'посл-ть цифр (\d+) и посл-ть пробелов, после цифр (\s+)'

        - '|'
        -- 'или'

        - '\d+\.'
        -- 'посл-ть цифр (\d+) и точку, после цифр (\.)'

        Итог: ['2025 ',  '13.', '10.', '2023 ', '1067758761498 ', '1. ', '1.', '1. ', '1.', '2. ', ...]"""

        result_head = re.findall(pattern_head, text)

        pattern_item = r'\d+\.\d+\.\s+|\d+\.\d+\s+'
        """ ['1.1. ', '1.2. ', '1.3. ', '1.4. ', '2.1. ', ...] """

        result_item = re.findall(pattern_item, text)

        pattern_other = r'\s\d+'
        """ [' 2025', ' 26', ' 91'] """
        result_other = re.findall(pattern_other, text)

        check_out = 0
        if len(result_head) != 0 and len(result_item) == 0 and len(result_other) == 0:
            check_out = 1
        
        """
            text = 1. Предмет Договора
            result_head: ['1. ']
            result_item: []
            result_other: []
            Итог: 1
        """
        return check_out

    def check_label(self, text_id):
        """Проверяет метку текста: ищет загаловок и отсеивает нумерацию страниц"""
        text_label = self.data['texts'][text_id]['label']
        check_out = 0
        if text_label == 'section_header':
            check_out = 1
        elif text_label in ['page_footer', 'page_header']:
            check_out = -1
        return check_out


    def create_id_head(self):
        """Ищет id заголовка документа"""
        """ [4, 10, 19, 36, 57, 72, 83, 87, 96, 104, 112, 122, 141, 144] """
        creat_arr = []
        for i in range(len(self.data['texts'])):
            if self.check_headings(i) == 1 and self.check_label(i) == 1:
                creat_arr.append(i)
        return creat_arr

    def print_id_head(self, arr_id_head):
        """
        4 -> 1. Предмет Договора (section_header)
        10 -> 2. Цена Договора и порядок расчетов. (section_header)`
        """
        for el in arr_id_head:
            print(f"{el} -> {self.data['texts'][el]['orig']} ({self.data['texts'][el]['label']})")

    def create_id_head_plus(self, arr_id_head):
        """ Создает пары 'глав' текста """
        """ [[0, 3], [4, 9], [10, 18], [19, 35], ... , [144, 428]] """
        creat_arr_plus = []
        creat_arr_plus.append([0, arr_id_head[0]-1])

        for i in range(len(arr_id_head)-1):
            creat_arr_plus.append([arr_id_head[i], arr_id_head[i+1]-1])

        creat_arr_plus.append([arr_id_head[-1], len(self.data['texts'])-1])
        return creat_arr_plus

    def print_text_id(self, start, end):
        """ Выводит по id текст, начиная с 'start' до 'end+1' """
        """ 
        1. Предмет Договора
        1.1. Заказчик  поручает...
        1.2. Требования,  предъявляемые...
        1.3. Проектная  и  рабочая...
        1.4. Содержание,  сроки...
        """
        for i in range(start, end+1):
            if(self.check_label(i) == -1):
                continue
            print(self.data['texts'][i]['orig'])
        print("\n")

    def print_id_head_plus(self, arr_id_head_plus, k=-1):
        """
        Text: 4 -> 9
        1. Предмет Договора
        1.1. Заказчик  поручает...
        1.2. Требования,  предъявляемые...
        1.3. Проектная  и  рабочая...
        1.4. Содержание,  сроки...
        """
        j = k
        if k == -1:
            k = len(arr_id_head_plus)-1
            j = 0

        for i in range(j, k+1):
            print(f"Text: {arr_id_head_plus[i][0]} -> {arr_id_head_plus[i][1]}")
            self.print_text_id(arr_id_head_plus[i][0], arr_id_head_plus[i][1])