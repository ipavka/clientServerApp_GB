import socket
import random
import json

from common.methods_utils import (
    connect_server,
    read_message,
    write_message,
    GREETINGS,
)
from common.config import (
    MAX_CONNECT,
    ACTION,
    PRESENCE,
    USER,
    ACCOUNT_NAME,
    TIME,
    RESPONSE,
    ERROR,
    BAD_REQ,
    MESSAGE_TEXT,
)


def validation_and_response(res: dict) -> dict:
    """ Валидация и ответ сообщения клиента """
    if (ACTION in res
            and res[ACTION] == PRESENCE
            and TIME in res
            and USER in res
            and res[USER][ACCOUNT_NAME] == 'Anonymous'):
        result = {
            RESPONSE: 200,
            MESSAGE_TEXT: random.choice(GREETINGS),
        }
        return result

    else:
        result = {
            RESPONSE: 400,
            ERROR: BAD_REQ
        }
        return result


def start_server():
    """ Запуск Сервера """
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    server.bind(connect_server())
    server.listen(MAX_CONNECT)

    while True:
        conn, address = server.accept()
        try:
            client_message = read_message(conn)
            server_response = validation_and_response(client_message)
            write_message(conn, server_response)
            conn.close()
        except (ValueError, json.JSONDecodeError):
            print('Ошибка декодирования сообщения клиента.')


if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        exit()
