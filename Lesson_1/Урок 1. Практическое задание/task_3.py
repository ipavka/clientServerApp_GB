"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""

WORDS = ['attribute', 'класс', 'функция', 'type']

# Мой вариант, не верный так как в условие нельзя использовать "encode decode"
for w in WORDS:
    try:
        print(f"Тип: {w.encode('ascii')},"
              f" Содержимое: '{w}',"
              f" Длина {len(w.encode('ascii'))}")
    except UnicodeEncodeError:
        print(f'Символ(ы) не входит в первый блок кодов из 128 символов ASCII')
        print(f'Слово "{w}" невозможно записать в байтовом типе с помощью маркировки b''')

print('*' * 50)
# Вариант преподавателя № 1
for el in WORDS:
    try:
        print(bytes(el, 'ascii'))
    except UnicodeEncodeError:
        print(f'Слово "{el}" невозможно записать в виде байтовой строки')


print('*' * 50)
# Вариант преподавателя № 2
for _el in WORDS:
    try:
        print('Слово записано в байтовом типе:', eval(f'b"{_el}"'))
    except SyntaxError:
        print(f'Слово "{_el}" невозможно записать в байтовой типе с помощью префикса b')
