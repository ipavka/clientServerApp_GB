import socket
import random
import json

from common.methods_utils import (
    connect_server,
    make_date,
    write_message,
    read_message,
    GREETINGS,
)
from common.config import (
    PRESENCE,
    TIME,
    USER,
    ACCOUNT_NAME,
    MESSAGE_TEXT,
    ACTION,
    RESPONSE,
    ERROR,
)


def prepare_request(name: str = 'Anonymous') -> dict:
    """ Функция формирует запрос/сообщение на сервер """
    result = {
        ACTION: PRESENCE,
        TIME: make_date(),
        MESSAGE_TEXT: random.choice(GREETINGS),
        USER: {
            ACCOUNT_NAME: name
        }
    }
    return result


def validation_server_response(res: dict) -> str:
    """ Валидация ответа сервера """
    if RESPONSE in res:
        if res[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {res[ERROR]}'
    raise ValueError


def run_client():
    """ Запуск клинта """
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    client.connect(connect_server())

    try:
        message_to_server = prepare_request()
        write_message(client, message_to_server)
        server_response = validation_server_response(read_message(client))
        print(server_response)
    except (ValueError, json.JSONDecodeError):
        print('Ошибка декодирования сообщения сервера.')


if __name__ == '__main__':
    try:
        run_client()
    except ConnectionResetError:
        exit()
    print(prepare_request())