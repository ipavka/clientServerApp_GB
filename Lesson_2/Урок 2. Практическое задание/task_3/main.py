"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import yaml

'''
Не совсем понял задание, сформировал файл как в примере, реализовал отображение
символов разными вариантами смотреть 'file_my.yaml'
'''

data = {
    'items': ['computer', 'printer', 'keyboard', 'mouse'],
    'items_price': {'computer': f'200{chr(8364)}-1000{chr(8364)}',
                    'computer1': '200\u20bd-1000\u20bd',
                    'keyboard': f'5{chr(8364)}-50{chr(8364)}',
                    'keyboard1': '5\u20bd-50\u20bd',
                    'mouse': f'4{chr(8364)}-7{chr(8364)}',
                    'mouse1': f'\u20bd-7\u20bd',
                    'printer': f'100{chr(8364)}-300{chr(8364)}',
                    'printer1': '100\u20bd-300\u20bd',
                    },
    'items_quantity': 4
}

# запись файла
with open('file_my.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

# чтение файла
with open('file_my.yaml', encoding='utf-8') as read_file:
    read_data = yaml.load(read_file, Loader=yaml.FullLoader)

# сравнение файлов
print("Данные совпадают" if data == read_data else "Что то не так")
