"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

import csv
import re
import os

FILE_NAME_ARR = [i for i in os.listdir() if i.startswith('info')]


def get_data() -> list:
    """
    parameters - хранение параметров значений
    main_data - итоговый массив для записи в csv
    :return: готовый массив для записи
    """
    parameters = {
        'Изготовитель системы': [],
        'Название ОС': [],
        'Код продукта': [],
        'Тип системы': [],
    }

    # добавляю заголовки для столбцов
    main_data = [[*parameters.keys()]]

    # добавить цифры для нумерации строк
    for i in range(len(FILE_NAME_ARR)):
        main_data.append([i + 1])

    # считываю, фильтрую(re) и записываю нужные данные в parameters
    for file_name in FILE_NAME_ARR:
        with open(file_name, 'r') as file:
            for el in file:
                fetch = re.search(r'([^:]*):\s+([^\n]+)', el)

                # проверка на пустые значения и совпадение заголовков
                if fetch and fetch[1] in parameters.keys():
                    value = fetch[1]  # значение
                    param = fetch[2].split()  # параметр

                    if len(param) > 2:
                        # сокращаю запись параметра "Название ОС"
                        param = fetch[2].split()[1:3]
                    parameters[value].append(' '.join(param))

    # вставка в нужном порядке данных из parameters
    for element in parameters.values():
        for i, _ in enumerate(element):
            main_data[i + 1].append(element[i])

    return main_data


def write_to_csv(name: str) -> None:
    """
    функция принимает название файла и записывает в csv
    data - данные из функции "get_data()"
    :param name: имя файла
    """
    data = get_data()

    with open(name, 'w', encoding='utf-8', newline='') as file:
        write = csv.writer(file)
        write.writerows(data)


if __name__ == '__main__':
    write_to_csv('main_report .csv')

