"""Простейший декоратор-функция с параметром"""

import time
import requests


def decorator(iters):
    """Внешняя функция (формально - декоратор)"""
    def real_decorator(func):
        """Сам декоратор"""
        def wrapper(*args, **kwargs):
            """Обертка"""
            total = 0
            for _ in range(iters):
                start = time.time()
                return_value = func(*args, **kwargs)
                end = time.time()
                total = total + (end-start)
            print(f'Среднее время выполнения: {round(total/iters, 2)} секунд')
            return return_value

        return wrapper
    return real_decorator


@decorator(iters=10)
def get_wp(url):
    """Запрос"""
    res = requests.get(url)
    return res


get_wp('https://google.com')
