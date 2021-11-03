"""Модуль modules"""

import subprocess
import chardet

ARGS = ['ping', 'yandex.ru']
YA_PING = subprocess.Popen(ARGS, stdout=subprocess.PIPE)

for line in YA_PING.stdout:
    result = chardet.detect(line)
    # line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode(result['encoding']).encode('utf-8').decode('utf-8'))


def run_ping(args):
    for item in args:
        # print(item)
        new_ping = subprocess.Popen(item, stdout=subprocess.PIPE)
        for line in new_ping.stdout:
            result = chardet.detect(line)
            line = line.decode(result['encoding']).encode('utf-8')
            print(line.decode('utf-8'))


ARGS = (['ping', 'youtube.com'], ['ping', 'ya.ru'])
run_ping(ARGS)