"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""

import chardet
import subprocess

ARGS = (
    ['ping', 'yandex.ru'],
    ['ping', 'youtube.com'],
    ['ping', 'gb.ru']
)

for arg in ARGS:
    ping_result = subprocess.Popen(arg, stdout=subprocess.PIPE)
    for site in ping_result.stdout:
        res = chardet.detect(site)
        print(site.decode(res['encoding']).encode('utf-8').decode('utf-8'))
