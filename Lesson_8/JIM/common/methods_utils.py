""" Общие методы для Сервера и Клиента """

from ipaddress import ip_address
import sys
import time
import socket
import json
import argparse
from random import randint

from .config import (
    ENCODING,
    MAX_LENGTH,
    DEFAULT_IP_ADDRESS,
    DEFAULT_PORT,
)
from .exceptions import IncorrectMode

from .decor import log

def get_ip_and_port() -> tuple[str, int]:
    """ Возвращает ip и порт из переданных значений,
    если нет применяет значения по умолчанию. Для Сервера
    """
    try:
        return sys.argv[1], int(sys.argv[2])
    except IndexError:
        return DEFAULT_IP_ADDRESS, DEFAULT_PORT


@log
def connect_server() -> tuple[str, int]:
    """ Валидация ip и порта
     Проверяет корректность ip адреса и порта,
     при неверном значении вызывает исключение. Для Сервера
    """
    try:
        server, port = get_ip_and_port()
        ip_address(server)
        if port < 1024 or port > 65535:
            raise ValueError('Порт должен быть в промежутке от 1024 до 65535')
        else:
            return server, port
    except ValueError as e:
        print(f'Не корректный ip адрес или порт\n{e}')
        sys.exit(1)


@log
def get_ip_port_and_mod() -> tuple[str, int, str]:
    """ Получение ip, порта и имя клиента. Для Клиента """
    sys_argv = argparse.ArgumentParser()
    sys_argv.add_argument('host', default=DEFAULT_IP_ADDRESS, nargs='?',)
    sys_argv.add_argument('port', type=int, default=DEFAULT_PORT, nargs='?')
    sys_argv.add_argument('-n', '--name', default=f'Anon_{randint(101, 300)}', nargs='?')

    result = sys_argv.parse_args(sys.argv[1:])
    host = result.host
    port = result.port
    mode = result.name

    return host, port, mode

@log
def connect_client() -> tuple[str, int, str]:
    """ Валидация ip и порта
     Проверяет корректность ip адреса и порта,
     при неверном значении вызывает исключение. Для Клиента
    """
    try:
        server, port, name_client = get_ip_port_and_mod()
        ip_address(server)
        if port < 1024 or port > 65535:
            raise ValueError('Порт должен быть в промежутке от 1024 до 65535')
        else:
            return server, port, name_client
    except ValueError as e:
        print(f'Не корректный ip адрес или порт\n{e}')
        sys.exit(1)


def make_date() -> str:
    """ Делает дату в формате 'datetime' """
    named_tuple = time.localtime()
    date = time.strftime("%Y/%m/%d %H:%M:%S", named_tuple)
    return date

@log
def write_message(sock_data: socket.socket, message: dict) -> None:
    """ Пишем сообщение """
    if not isinstance(message, dict):
        raise ValueError
    dumps_message = json.dumps(message)
    result = dumps_message.encode(ENCODING)
    sock_data.send(result)

@log
def read_message(sock_data: socket.socket) -> dict:
    """ Читаем сообщение """
    data = sock_data.recv(MAX_LENGTH)
    if isinstance(data, bytes):
        decode_response = data.decode(ENCODING)
        result = json.loads(decode_response)
        if isinstance(result, dict):
            return result
        raise ValueError
    raise ValueError


if __name__ == '__main__':
    pass

