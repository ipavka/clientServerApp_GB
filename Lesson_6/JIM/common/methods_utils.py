""" Общие методы для Сервера и Клиента """

from ipaddress import ip_address
import sys
import time
import socket
import json

from .config import (
    ENCODING,
    MAX_LENGTH,
    DEFAULT_IP_ADDRESS,
    DEFAULT_PORT,
)
from .decor import log

def get_ip_and_port() -> tuple[str, int]:
    """ Возвращает ip и порт из переданных значений,
    если нет применяет значения по умолчанию.
    """
    try:
        return sys.argv[1], int(sys.argv[2])
    except IndexError:
        return DEFAULT_IP_ADDRESS, DEFAULT_PORT

@log
def connect_server() -> tuple[str, int]:
    """ Валидация ip и порта
     Проверяет корректность ip адреса и порта,
     при неверном значении вызывает исключение.
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


def make_date() -> str:
    """ Делает дату в формате 'datetime' """
    named_tuple = time.localtime()
    date = time.strftime("%Y/%m/%d %H:%M:%S", named_tuple)
    return date

@log
def write_message(sock_data: socket.socket, message) -> None:
    """ Пишем сообщение """
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


# Варианты приветствий и ответов
GREETINGS = (
    "hey", "good morning", "hello", "Шалом", "Привет Сервер",
    "good evening", "morning", "evening", "hi",
    "whatsapp")

if __name__ == '__main__':
    pass

