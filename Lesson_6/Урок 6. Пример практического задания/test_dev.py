import sys
import time
import requests
import traceback
import inspect
from pprint import pprint

st = "C:/PycharmProjects/Geekbrains/Geekbrains_2/client_server_app/Lesson_6/" \
     "Урок 6. Пример практического задания/server.py"


# for i, j in enumerate(st):
#     print(i, j)

# print(sys.argv[0].find('client.py'))
# print(sys.argv[0].find('test_dev.py'))
# print(sys.argv)
# print(sys.argv[0])
# print(len(sys.argv))

def decorator_function(func):
    def wrapper():
        print('Функция-обёртка!ё')
        print(f'Оборачиваемая функция: {func}')
        print('Выполняем обёрнутую функцию...')
        func()
        print('Выходим из обёртки')

    return wrapper


@decorator_function
def hello_world():
    print('Hello world!')


# hello_world()

def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'[*] Время выполнения: {end - start} секунд.')
        print(traceback.format_stack()[0].strip().split()[-1])
        print(inspect.stack())
        print(inspect.stack()[1][3])
        print('*' * 50)
        return result
    return wrapper


@benchmark
def fetch_webpage(url):
    webpage = requests.get(url)
    return webpage.text[:200]


pprint(fetch_webpage('https://google.com'))
