import socket
import random
from loguru import logger
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
        logger.info(f'Serving on {address[0]} port {address[1]}')
        try:
            client_message = read_message(conn)
            logger.info(f'Полное сообщение от клиента: {client_message}')

            server_response = validation_and_response(client_message)
            write_message(conn, server_response)
            conn.close()
        except (ValueError, json.JSONDecodeError):
            print('Ошибка декодирования сообщения клиента.')


if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        logger.info('Stop server by keyboard...')
    exit()
