"""Простейший декоратор-функция"""

import time
import requests


def decorator(func):
    """Сам декоратор"""
    def wrapper(*args, **kwargs):
        """Обертка"""
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print(f'Отправлен запрос на адрес {args[0]}. '
              f'Время выполнения: {round(end-start, 2)} секунд')
        # обертка может возвращать и некий результат
        return return_value
    return wrapper


@decorator
def get_wp(url):
    """Делаем запрос"""
    res = requests.get(url)
    return res


print(get_wp('https://google.com'))
