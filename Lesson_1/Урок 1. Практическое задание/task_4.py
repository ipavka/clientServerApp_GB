"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

words = ['разработка', 'администрирование', 'protocol', 'standard']
words_bytes = []
words_bytes_1 = []


for w in words:
    words_bytes.append(bytes(w, 'utf-8'))  # вариант 1
    words_bytes_1.append(w.encode())  # вариант 2

for i in words_bytes:
    print(f'Обратное преобразование: {i.decode()}')

print(f'Слова в байтовом представлении {words_bytes}')
print(f'Слова в байтовом представлении_1 {words_bytes_1}')

